# DATA_ENG 300 – Homework 1: Aircraft Dataset Cleaning & Analysis  
**Author**: Marcus Van Mieghem

---

## Files Included

- `DATA_ENG300_HW1_Aircraft.ipynb`: Main notebook containing all code which includes data cleaning, visualizations, and imputation methods.
- `DATA_ENG300_HW1_Aircraft.pdf`: PDF file containing my written answers and analysis.
- `README.md`: This file.

---

## How to Run the Notebook

1. Open `VanMieghem_Homework1.ipynb` in Jupyter Notebook, JupyterLab, or VS Code.
2. Ensure the following Python packages are installed:
    - pandas  
    - numpy  
    - matplotlib.pyplot  
    - seaborn  
    - scipy.stats
    - scipy
3. Run all cells in order.

---

## Expected Outputs

When executed, the notebook will:

	•	Output a summary of the dataset’s structure and missing values
	•	Output a cleaned CARRIER column with missing values imputed
	•	Output a cleaned CARRIER_NAME column with consistent entries
	•	Output imputed values for MANUFACTURE_YEAR, NUMBER_OF_SEATS, CAPACITY_IN_POUNDS, and AIRLINE_ID
	•	Output standardized values for MANUFACTURER, MODEL, AIRCRAFT_STATUS, and OPERATING_STATUS
	•	Output a cleaned dataset with missing rows dropped from key columns
	•	Output histograms and skewness values for NUMBER_OF_SEATS and CAPACITY_IN_POUNDS
	•	Output Box-Cox transformed versions of NUMBER_OF_SEATS and CAPACITY_IN_POUNDS
	•	Output a new SIZE column categorizing aircraft by seat count quartiles
	•	Output proportion tables and bar plots comparing OPERATING_STATUS and AIRCRAFT_STATUS by aircraft size

---

## Notes

The notebook is divided into clearly labeled tasks (Task 0–Task 5), each with relevant sub-tasks and explanations.