import numpy as np  # This line imports the NumPy library
import pandas as pd
import os
from statsmodels.stats.outliers_influence import variance_inflation_factor
from functools import reduce
import statsmodels.api as sm

# Dictionaries for datasets
independent_datasets = {
    '^IXIC.csv': 'Close',
    '^VIX.csv': 'Close',
    'BOGMBASE.csv': 'BOGMBASE',
    'CPIAUCSL.csv': 'CPIAUCSL',
    'Crude Oil.csv': 'Price',
    'DGS2.csv': 'DGS2',
    'DGS5.csv': 'DGS5',
    'DGS10.csv': 'DGS10',
    'DGS30.csv': 'DGS30',
    'DJI.csv': 'Close*',
    'FEDFUNDS.csv': 'FEDFUNDS',
    'Gold.csv': 'Price',
    'GSPC - S&P 500.csv': 'Close*',
    'UNRATE.csv': 'UNRATE',
    'USSTHPI.csv': 'USSTHPI',
    'WM2NS.csv': 'WM2NS'
}
data_directory = 'Data'
results_directory = os.path.join(data_directory, 'Result')
os.makedirs(results_directory, exist_ok=True)

def load_data(file_name, column_name):
    file_path = os.path.join(data_directory, file_name)
    df = pd.read_csv(file_path)
    df["DATE"] = pd.to_datetime(df["DATE"], errors='coerce')
    df.set_index("DATE", inplace=True)

    # Standardize column names by removing spaces and special characters
    df.columns = df.columns.str.replace(' ', '').str.replace('*', '').str.replace('(', '').str.replace(')', '').str.lower()

    # Print columns for debugging
    print(f"Columns in {file_name}: {df.columns.tolist()}")

    # Define standardized column name based on provided dictionary mapping
    standardized_column_name = column_name.lower().replace(' ', '').replace('*', '').replace('(', '').replace(')', '')

    # Check if the standardized column name exists
    if standardized_column_name not in df.columns:
        error_msg = f"Column '{standardized_column_name}' not found in {file_name}. Available columns: {df.columns.tolist()}"
        raise KeyError(error_msg)

    # Select and rename the column to avoid conflicts during merging
    new_col_name = f"{standardized_column_name}_{file_name.replace('.csv', '')}"
    df.rename(columns={standardized_column_name: new_col_name}, inplace=True)

    # Ensure the column is returned with the new name
    return df[[new_col_name]]

# Update other parts of your script accordingly to handle these debugging outputs and corrections.


data_frames = [load_data(file, name) for file, name in independent_datasets.items()]

# Merge all dataframes on the index (usually DATE)
merged_data = reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True, how='outer'), data_frames)

# Handle missing values
merged_data.ffill(inplace=True)  # Forward fill
merged_data.bfill(inplace=True)  # Backward fill to handle NaNs at the start
merged_data.replace([np.inf, -np.inf], np.nan, inplace=True)  # Replace infinities with NaN
merged_data.dropna(inplace=True)  # Drop rows with NaNs that might have been caused by infinite replacements

# Ensure all data is float type for VIF computation
merged_data = merged_data.apply(pd.to_numeric, errors='coerce')

# It's important to again drop any remaining NaNs that might have been introduced by type conversion or earlier operations
merged_data.dropna(inplace=True)

# Add a constant for VIF calculation
merged_data = sm.add_constant(merged_data)

# Calculate VIF for each independent variable
vif_data = pd.DataFrame()
vif_data["variable"] = merged_data.columns
vif_data["VIF"] = [variance_inflation_factor(merged_data.values, i) for i in range(merged_data.shape[1])]

print(vif_data)

# Save VIF data to CSV in the results directory
vif_data.to_csv(os.path.join(results_directory, 'vif_results.csv'), index=False)
