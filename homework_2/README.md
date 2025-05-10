# DATA_ENG 300 – Homework 2: Healthcare Database

**Author**: Marcus Van Mieghem

------------------------------------------------------------------------

## Files Included

-   `DATA_ENG300_HW2_HealthcareDatabase_PartI.ipynb`: Notebook containing all code which creates a SQL database, runs queries, generates charts for analysis, and exports CSV files for Part II.
-   `DATA_ENG300_HW2_HealthcareDatabase_PartII.ipynb`: Notebook containing all code for creating and querying a NoSQL database (Cassandra), importing data, and producing analysis charts.
-   `DATA_ENG300_HW2_Healthcare.pdf`: PDF file containing my written answers and analysis.
-   `ADMISSIONS.csv, D_ICD_PROCEDURES.csv, DRGCODES.csv, ICUSTAYS.csv, PATIENTS.csv, PRESCRIPTIONS.csv, PROCEDURES_ICD.csv`: Original raw MIMIC-III demo dataset tables used for database construction and querying in Part I.
-   `admissions_with_age_partII_ueb9720.csv`: Exported CSV containing patient age group data for use in NoSQL analysis (Question 2).
-   `drug_type_ethnicity_partII_ueb9720.csv`: Exported CSV containing prescription data categorized by drug type and ethnicity (Question 1).
-   `patient_ICU_duration_partII_ueb9720.csv`: Exported CSV with ICU stay duration metrics, gender, and ethnicity (Question 3).
-   `README.md`: This file.

------------------------------------------------------------------------

## How to Run the Notebooks (via Docker)

1.  **Build and run the Docker container**

2.  **Open the notebooks**:

    -   `DATA_ENG300_HW2_Healthcare_PartI.ipynb`: for all DuckDB-based relational analysis\
    -   `DATA_ENG300_HW2_Healthcare_PartII.ipynb`: for all Cassandra-based NoSQL analysis

3.  **Insert your personal Cassandra credentials and keyspace info** in the first cell of `DATA_ENG300_HW2_Healthcare_PartII.ipynb`

4.  **Ensure the following Python packages are installed in your environment**:

### Part I (Relational / DuckDB)

-   `pandas`
-   `matplotlib`
-   `seaborn`
-   `duckdb`

### Part II (Non-relational / Cassandra)

-   `pandas`
-   `matplotlib`
-   `seaborn`
-   `csv` (standard library)
-   `ssl` (standard library)
-   `boto3`
-   `cassandra-driver`
-   `cassandra-sigv4`

5.  **Run all cells in each notebook from top to bottom**:
    -   **Part I** performs relational data processing, joins, and exports CSVs.
    -   **Part II** loads those CSVs into Amazon Keyspaces (Cassandra), performs NoSQL queries, and reproduces analysis charts.

------------------------------------------------------------------------

## Expected Outputs

When executed, the notebooks will:

### Part I (Relational / DuckDB)

-   Output a relational database containing all raw MIMIC-III CSV tables
-   Query from the database in order to create summaries about:
    -   Drug type by patient ethnicity
    -   Procedures performed by age group
    -   ICU stay duration by gender and ethnicity
-   Output visualizations (bar plots, box plots, histograms) for each analysis question
-   Export cleaned CSVs to be used in Part II (NoSQL)

### Part II (NoSQL / Cassandra)

-   Connect to Amazon Keyspaces
-   Upload raw, non-aggregated data from Part I into separate Cassandra tables (one per analysis question)
-   Extract the raw data back from Cassandra using select queries
-   Perform post-query analysis in Python using Pandas and Seaborn
-   Reproduce the same summary statistics and visualizations as in Part I to verify results match

------------------------------------------------------------------------

## Notes

-The notebooks are divided into clearly labeled sections for each analysis question
-The CSV to be used in Part II are included. If you would like to regenerate, change the when running the .to_csv() cells.
