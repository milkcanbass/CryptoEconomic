import pandas as pd
import statsmodels.api as sm
import numpy as np
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
    'DJI.csv': 'Close',
    'FEDFUNDS.csv': 'FEDFUNDS',
    'Gold.csv': 'Price',
    'GSPC - S&P 500.csv': 'Close*',
    'UNRATE.csv': 'UNRATE',
    'USSTHPI.csv': 'USSTHPI',
    'WM2NS.csv': 'WM2NS',
    'BTC-USD.csv': 'Close',  # Now treated as another independent variable
    # Removed ETH-USD.csv from here as it becomes the main dataset
}

def load_and_prepare_data(file_path, value_column):
    df = pd.read_csv(file_path)
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    df.dropna(subset=['DATE'], inplace=True)
    df.set_index('DATE', inplace=True)
    return df[[value_column]]

def merge_dataframes(main_df, other_df, file_name, column_name):
    other_df = other_df.rename(columns={column_name: f"{column_name}_{file_name.replace('.csv', '')}"})
    return main_df.join(other_df, how='outer')

def ensure_numeric(df):
    for column in df.columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')
    return df

def save_regression_results(results, directory, filename):
    summary = results.summary()
    with open(os.path.join(directory, filename), 'w') as f:
        f.write(summary.as_text())

# Directory setup
data_directory = 'Data'
result_directory = os.path.join(data_directory, 'Results')
if not os.path.exists(result_directory):
    os.makedirs(result_directory)

# Load and prepare main DataFrame (ETH-USD now the main dataset)
main_file = 'ETH-USD.csv'
main_path = os.path.join(data_directory, main_file)
main_df = load_and_prepare_data(main_path, 'Close')
main_df = ensure_numeric(main_df)

# Merge and clean data
for file_name, column_name in datasets.items():
    file_path = os.path.join(data_directory, file_name)
    other_df = load_and_prepare_data(file_path, column_name)
    other_df = ensure_numeric(other_df)
    main_df = merge_dataframes(main_df, other_df, file_name, column_name)

# Check and handle NaNs before regression
main_df.ffill(inplace=True)
main_df.replace([np.inf, -np.inf], np.nan, inplace=True)
main_df.dropna(inplace=True)

# Ensure there are no NaNs or Infs in the data
if main_df.isnull().any().any() or np.isinf(main_df.values).any():
    print("Data still contains NaNs or infinite values after cleaning.")
else:
    X = sm.add_constant(main_df.drop(columns='Close'))  # Exclude the dependent variable column
    y = main_df['Close']  # Dependent variable is now ETH closing prices
    if not X.empty:
        model = sm.OLS(y, X)
        results = model.fit()

        # Save results
        result_filename = 'linear_regression_ETH_USD_with_others.txt'
        save_regression_results(results, result_directory, result_filename)
    else:
        print("DataFrame X is empty after processing.")
