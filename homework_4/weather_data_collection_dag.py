from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd
import boto3
import time
import os

# Constants
WEATHER_STATIONS = ["KORD", "KENW", "KMDW", "KPNT"]
BASE_URL = "https://api.weather.gov/stations/{station}/observations/latest"
S3_BUCKET = "" # Replace with your S3 bucket name
S3_DIRECTORY = "weather_data"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

def collect_weather_data(**context):
    collected_data = []
    time_of_collection = datetime.utcnow().isoformat()

    for station in WEATHER_STATIONS:
        url = BASE_URL.format(station=station)
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json().get("properties", {})
            collected_data.append({
                "timeOfCollection": time_of_collection,
                "timestamp": json_data.get("timestamp"),
                "station": station,
                "temperature": json_data.get("temperature", {}).get("value"),
                "dewpoint": json_data.get("dewpoint", {}).get("value"),
                "windSpeed": json_data.get("windSpeed", {}).get("value"),
                "barometricPressure": json_data.get("barometricPressure", {}).get("value"),
                "visibility": json_data.get("visibility", {}).get("value"),
                "precipitationLastHour": json_data.get("precipitationLastHour", {}).get("value"),
                "relativeHumidity": json_data.get("relativeHumidity", {}).get("value"),
                "heatIndex": json_data.get("heatIndex", {}).get("value"),
            })
        time.sleep(2)  # avoid rate limits

    df = pd.DataFrame(collected_data)

    # Create a unique filename
    timestamp_str = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    filename = f"weather_data_{timestamp_str}.csv"
    filepath = f"/tmp/{filename}"
    df.to_csv(filepath, index=False)

    # Upload to S3
    s3 = boto3.client('s3')
    s3.upload_file(filepath, S3_BUCKET, f"{S3_DIRECTORY}/{filename}")
    os.remove(filepath)  # optional: clean up

with DAG(
    dag_id="weather_data_collection_dag",
    default_args=default_args,
    description="Collect weather data every 2 hours and store in S3",
    schedule_interval="0 */2 * * *",  # Every 2 hours
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["weather", "s3", "api"],
) as dag:

    collect_and_store = PythonOperator(
        task_id="collect_weather_data",
        python_callable=collect_weather_data,
        provide_context=True,
    )

    collect_and_store
