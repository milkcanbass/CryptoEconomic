import pandas as pd
import os

# Dictionary mapping each dataset file name to the relevant column name for analysis
datasets = {
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


def read_and_describe(directory, datasets):
    all_stats = []

    for file, target_col in datasets.items():
        file_path = os.path.join(directory, file)
        df = pd.read_csv(file_path)

        # Standardize column names: remove spaces and special characters for easier matching
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '').str.replace('.', '').str.replace('*', '').str.replace(',', '')

        # Correct target column based on dictionary mapping
        target_col = target_col.lower().replace(' ', '').replace('.', '').replace('*', '').replace(',', '')
        if target_col not in df.columns:
            print(f"Target column '{target_col}' not found in {file}, skipping.")
            continue

        # Convert to numeric, coercing errors
        df[target_col] = pd.to_numeric(df[target_col], errors='coerce')

        # Calculate descriptive statistics and round to 2 decimal places
        stats = df[target_col].describe().round(2)
        stats.name = target_col.capitalize() + '_' + file.split('.')[0]
        all_stats.append(stats.to_frame())

    if all_stats:
        result = pd.concat(all_stats, axis=1)
        return result
    return pd.DataFrame()

def save_to_csv(df, directory, subfolder='Result', filename='descriptive_statistics.csv'):
    result_directory = os.path.join(directory, subfolder)
    if not os.path.exists(result_directory):
        os.makedirs(result_directory)
    
    file_path = os.path.join(result_directory, filename)
    try:
        df.to_csv(file_path)
        print(f"Descriptive statistics saved to {file_path}")
    except Exception as e:
        print(f"Failed to save the file due to: {e}")

directory = 'Data'
try:
    descriptive_stats = read_and_describe(directory, datasets)
    if not descriptive_stats.empty:
        save_to_csv(descriptive_stats, directory)
    else:
        print("No descriptive statistics were generated.")
except Exception as e:
    print(f"An error occurred during the processing: {e}")