# DATA_ENG 300 – Homework 3: MapReduce and Spark

**Author**: Marcus Van Mieghem

------------------------------------------------------------------------

## Files Included

-   `DATA_ENG300_HW3_MapReduce_and_Spark.ipynb`: Notebook containing all code for this assignment, including:
    -   TF-IDF calculation using PySpark and MapReduce principles
    -   Soft-margin SVM loss implementation in NumPy
    -   SVM prediction logic using PySpark
    -   Embedded comments for clarity
-   `README.md`: This file

> **Note**: Raw datasets (`agnews_clean.csv`, `data_for_svm.csv`, `w.csv`, `bias.csv`) are not included in the submission. These files are downloaded using `curl` commands provided at the top of the notebook.

------------------------------------------------------------------------

## How to Run the Notebook (via Docker or Local Python)

1.  **Ensure you have the required Python libraries installed:**
    -   `pyspark`
    -   `pandas`
    -   `numpy`
    -   `nltk`
2.  **Launch the notebook (homework3_annotated.ipynb) and run all cells in order.**

## Expected Outputs

When executed, the notebook will:

### Part I: TF-IDF via MapReduce (PySpark)

-   Load the `agnews_clean.csv` dataset
-   Clean the data by removing stopwords and short words
-   Compute:
    -   Term Frequency (TF)
    -   Document Frequency (DF)
    -   Inverse Document Frequency (IDF)
    -   TF-IDF values for each word in each document
-   Display TF-IDF results for the first 5 documents, showing which words are most important in each

### Part II: SVM Loss and Prediction

-   Load feature data (`data_for_svm.csv`), weights (`w.csv`), and bias (`bias.csv`)
-   Calculate the soft-margin SVM loss using NumPy, combining hinge loss and L2 regularization
-   Predict class labels using the SVM decision rule with PySpark
-   Save the predictions to a CSV directory named `svm_predictions/`

------------------------------------------------------------------------

## Notes

-   All code is contained in a single notebook: `DATA_ENG300_HW3_MapReduce_and_Spark.ipynb`, the notebook is clearly organized into different sections for each problem
-   Each cell is clearly commented to explain the purpose and logic of the code
-   No data files are included in the repo; all datasets are downloaded using `curl` as shown in the notebook
-   Output directories (like `svm_predictions/`) are created automatically when the notebook is run
