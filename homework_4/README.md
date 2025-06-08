# DATA_ENG 300 – Homework 4: Apache Airflow

**Author**: Marcus Van Mieghem

------------------------------------------------------------------------

## Files Included

-   `weather_data_collection_dag.py` – Collects weather data every 2 hours from four NOAA stations and stores results in `.csv` files in S3.
-   `daily_weather_dashboard_dag.py` – Generates daily graphs (temperature, visibility, relative humidity) and uploads `.png` files to S3.
-   `weather_temp_prediction_dag.py` – Trains linear regression models after 20 and 40 hours of data; saves 8-hour temperature forecasts to S3.
-   `README.md` – This file.

> **Note**: All DAGs were deployed to MWAA and configured to stop execution after 48 hours.

------------------------------------------------------------------------

## How to Deploy and Run

1.  **Create a S3 bucket and a Airflow instance**\
    Insert S3 bucket name in all Python files.

2.  **Upload DAGs**\
    Place all `.py` DAG files into the `dags/` directory of your S3 bucket connected to MWAA.

3.  **Upload requirements.txt**\
    Upload this file to the \*\*plugins/requirements.txt\*\* path in your MWAA environment’s S3 bucket, then update the environment to install these packages.

4.  **Trigger DAGs**\
    Each DAG was scheduled to run automatically:

-   `weather_data_collection_dag`: every 2 hours
-   `daily_weather_dashboard`: daily
-   `weather_temp_prediction`: hourly (but only runs at 20h and 40h)

------------------------------------------------------------------------

## DAG Descriptions

### `weather_data_collection_dag.py`

-   Pulls weather data every 2 hours from:
-   `KORD`, `KENW`, `KMDW`, `KPNT`
-   Extracted fields:
-   `timestamp`, `station`, `temperature`, `dewpoint`, `windSpeed`, `barometricPressure`, `visibility`, `precipitationLastHour`, `relativeHumidity`, `heatIndex`
-   Saves `.csv` files to:\
    `s3://bucket_name/weather_data/`

### `daily_weather_dashboard.py`

-   Combines `.csv` files from the same UTC day
-   Creates 3 graphs:
-   Temperature
-   Visibility
-   Relative Humidity
-   All four stations plotted together on the same time axis
-   Saves `.png` files to:\
    `s3://``bucket_name``/output_graphs/`

### `weather_temp_prediction.py`

-   Triggers only after 20 or 40 hours of data collected (based on `timeOfCollection`)
-   Trains a **Linear Regression** model per station
-   Predicts **next 8 hours** of temperature in **30-minute increments**
-   Uploads results to:\
    `s3://``bucket_name``/predictions/`

------------------------------------------------------------------------

## Notes

-   Each DAG was written to fail gracefully and includes logging.
-   The Airflow web UI was used to monitor run times, outputs, and status.
-   All DAGs include a hard `end_date` or were manually toggled off after 48 hours to meet project constraints.
-   The linear regression model was designed to run exactly twice (at \~20h and \~40h), matching the assignment spec.
