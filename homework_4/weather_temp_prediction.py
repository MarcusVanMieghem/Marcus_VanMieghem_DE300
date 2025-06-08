from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import boto3

# ─────── CONSTANTS ────────────────────────────────────────────────────────────

S3_BUCKET = "" # Replace with your S3 bucket name
DATA_DIR  = "weather_data"
PRED_DIR  = "predictions"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# ─────── TRAIN & PREDICT FUNCTION ─────────────────────────────────────────────

def train_and_upload(**context):
    """
    1) Download & combine all CSVs in s3://vanmieghem-mwaa/weather_data/
    2) Compute hours_elapsed since first timeOfCollection (UTC).
    3) If (20 ≤ hours_elapsed < 21) → run 20h branch.
       Else if (40 ≤ hours_elapsed < 41) → run 40h branch.
       Else, skip and exit.
    4) For each station: fit LinearRegression(temperature ~ timestamp_seconds).
    5) Predict next 8h (half-hour steps), write CSV, upload to s3://vanmieghem-mwaa/predictions/.
    """

    s3 = boto3.client("s3")

    # 1) List & download CSVs
    resp = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=f"{DATA_DIR}/")
    if "Contents" not in resp:
        print("⚠️ No objects found under weather_data/. Exiting.")
        return

    keys = [obj["Key"] for obj in resp["Contents"] if obj["Key"].endswith(".csv")]
    if not keys:
        print("⚠️ No CSV files found in weather_data/. Exiting.")
        return

    dfs = []
    for key in keys:
        print(f"📥 Downloading {key} …")
        obj = s3.get_object(Bucket=S3_BUCKET, Key=key)
        df = pd.read_csv(obj["Body"])
        dfs.append(df)

    df_all = pd.concat(dfs, ignore_index=True)

    # 2) Parse timeOfCollection as UTC → naive datetime
    df_all["timestamp"] = (
        pd.to_datetime(df_all["timeOfCollection"], utc=True)
          .dt.tz_localize(None)
    )

    earliest = df_all["timestamp"].min()
    now_utc = datetime.utcnow()
    hours_elapsed = (now_utc - earliest).total_seconds() / 3600.0
    print(f"⌚ Hours elapsed since first data: {hours_elapsed:.2f}")

    # 3) Determine which branch to run
    if 20.0 <= hours_elapsed < 21.0:
        suffix = "20h"
        print("▶️ Running 20 h training branch.")
    elif 40.0 <= hours_elapsed < 41.0:
        suffix = "40h"
        print("▶️ Running 40 h training branch.")
    else:
        print("⏭ Elapsed time not in [20,21) or [40,41). Skipping training.")
        return

    # 4) Train + predict per station
    predictions = []
    for station in df_all["station"].unique():
        df_st = df_all[df_all["station"] == station].dropna(subset=["temperature"])
        if df_st.shape[0] < 2:
            print(f"⚠️ Not enough data for station {station}, skipping.")
            continue

        # Convert timestamp to numeric (seconds since epoch)
        X = df_st["timestamp"].map(lambda d: d.timestamp()).values.reshape(-1, 1)
        y = df_st["temperature"].values.reshape(-1,)

        model = LinearRegression().fit(X, y)

        last_time = df_st["timestamp"].max()
        future_times = [
            last_time + timedelta(minutes=30 * i) for i in range(1, 17)
        ]

        X_future = np.array([ft.timestamp() for ft in future_times]).reshape(-1, 1)
        y_pred = model.predict(X_future)

        for ft, temp_pred in zip(future_times, y_pred):
            predictions.append({
                "station": station,
                "predictedTime": ft.isoformat(),
                "predictedTemperature": float(temp_pred),
            })

    if not predictions:
        print("⚠️ No predictions generated. Exiting.")
        return

    # 5) Write CSV & upload
    pred_df = pd.DataFrame(predictions)
    file_timestamp = now_utc.strftime("%Y%m%dT%H%M%S")
    filename = f"predictions_{file_timestamp}_{suffix}.csv"
    csv_bytes = pred_df.to_csv(index=False).encode("utf-8")

    print(f"📝 Uploading CSV to s3://{S3_BUCKET}/{PRED_DIR}/{filename}")
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=f"{PRED_DIR}/{filename}",
        Body=csv_bytes,
        ContentType="text/csv"
    )
    print(f"✅ Uploaded predictions to s3://{S3_BUCKET}/{PRED_DIR}/{filename}")

# ─────── DAG DEFINITION ────────────────────────────────────────────────────────

with DAG(
    dag_id="weather_temp_prediction",
    default_args=default_args,
    description="Train temperature-forecast model at 20h/40h milestones, upload CSVs to S3",
    schedule_interval="@hourly",           # runs every hour (UTC)
    start_date=datetime(2025, 6, 5, 0, 0), # adjust as needed; catchup=False means no backfill
    catchup=False,
    tags=["weather", "model", "prediction"],
) as dag:

    train_predict = PythonOperator(
        task_id="train_and_predict",
        python_callable=train_and_upload,
        provide_context=True,
    )

    train_predict
