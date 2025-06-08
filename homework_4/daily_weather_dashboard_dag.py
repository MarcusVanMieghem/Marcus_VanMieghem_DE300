from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import boto3
from io import BytesIO
import matplotlib.pyplot as plt
import pendulum

# ─────── DAG SETTINGS ────────────────────────────────────────────────────────

# We still need local tz only to label plots correctly. 
# But for scheduling, we'll anchor run times in UTC.
local_tz = pendulum.timezone("America/Chicago")

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

S3_BUCKET = "" # Replace with your S3 bucket name
DATA_DIR = "weather_data"     # folder where hourly CSVs live
OUTPUT_DIR = "output_graphs"  # folder where we write PNGs

FIELDS_TO_PLOT = {
    "temperature": "Temperature (°C)",
    "visibility": "Visibility (m)",
    "relativeHumidity": "Relative Humidity (%)"
}

# ─────── DAG FUNCTION ────────────────────────────────────────────────────────

def create_and_upload_graphs(execution_date, **kwargs):
    """
    1) List all CSVs in s3://vanmieghem-mwaa/weather_data/ that contain run_date (UTC→Chicago).
    2) Combine them, convert timeOfCollection (UTC) to Chicago time.
    3) Plot three PNGs (temperature / visibility / relativeHumidity) with line+dot.
    4) Upload each PNG to s3://vanmieghem-mwaa/output_graphs/.
    """
    s3 = boto3.client("s3")

    # 1) “execution_date” is a naive UTC datetime for the DAG run (e.g. 2025-06-06 00:00 UTC).
    #    Convert it to Chicago to figure out which “calendar day” to use.
    run_date = execution_date.astimezone(local_tz).strftime("%Y%m%d")

    # 2) List all objects under DATA_DIR/ and filter by run_date
    resp = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=f"{DATA_DIR}/")
    if "Contents" not in resp:
        print(f"⚠️ No objects found under {DATA_DIR}/ in S3.")
        return

    daily_keys = [
        obj["Key"]
        for obj in resp["Contents"]
        if (run_date in obj["Key"] and obj["Key"].endswith(".csv"))
    ]
    if not daily_keys:
        print(f"⚠️ No weather CSVs found for date {run_date}.")
        return

    # 3) Download each CSV, build one big DataFrame
    dfs = []
    for key in daily_keys:
        print(f"📥 Downloading {key} ...")
        obj = s3.get_object(Bucket=S3_BUCKET, Key=key)
        df = pd.read_csv(obj["Body"])
        dfs.append(df)

    df_all = pd.concat(dfs, ignore_index=True)

    # 4) Convert “timeOfCollection” (which is UTC) into America/Chicago
    df_all["timestamp"] = (
        pd.to_datetime(df_all["timeOfCollection"], utc=True)
          .dt.tz_convert(local_tz)
          .dt.tz_localize(None)  # drop tzinfo, so Matplotlib shows just “HH:MM” Chicago time
    )

    # 5) Plot each field (temperature, visibility, relativeHumidity)
    for field, ylabel in FIELDS_TO_PLOT.items():
        plt.figure(figsize=(10, 6))

        for station in df_all["station"].unique():
            df_station = df_all[df_all["station"] == station]
            plt.plot(
                df_station["timestamp"],
                df_station[field],
                marker="o",
                linestyle="-",
                label=station
            )

        plt.title(f"{ylabel} on {run_date}")
        plt.xlabel("Time (America/Chicago)")
        plt.ylabel(ylabel)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Save figure to an in‐memory buffer
        img_buf = BytesIO()
        plt.savefig(img_buf, format="png")
        img_buf.seek(0)

        # 6) Upload PNG buffer to S3
        output_key = f"{OUTPUT_DIR}/{field}_{run_date}.png"
        s3.put_object(
            Bucket=S3_BUCKET,
            Key=output_key,
            Body=img_buf,
            ContentType="image/png"
        )
        print(f"✅ Uploaded graph to s3://{S3_BUCKET}/{output_key}")

        plt.close()

# ─────── DAG DEFINITION ────────────────────────────────────────────────────────

with DAG(
    dag_id="daily_weather_dashboard",
    default_args=default_args,
    description="Combine daily weather CSVs, plot, and upload PNGs to S3",
    schedule_interval="@daily",             # fires at 00:00 UTC every day
    start_date=datetime(2025, 6, 5, 0, 0),  # the first “00:00 UTC” run is 2025-06-03 00:00 UTC 
    catchup=False,
    tags=["weather", "dashboard", "visualization"],
) as dag:

    generate_dashboard = PythonOperator(
        task_id="create_weather_dashboard",
        python_callable=create_and_upload_graphs,
        provide_context=True,
    )

    generate_dashboard
