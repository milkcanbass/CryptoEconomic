import numpy as np
import pandas as pd
import os
from statsmodels.stats.outliers_influence import variance_inflation_factor
from functools import reduce
import statsmodels.api as sm

# Dictionaries for datasets
independent_datasets = {
    'ETH-USD.csv': 'Close',
    'BTC-USD.csv': 'Close',
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
    df.columns = df.columns.str.replace(' ', '').str.replace('*', '').str.replace('(', '').str.replace(')', '').str.lower()
    standardized_column_name = column_name.lower().replace(' ', '').replace('*', '').replace('(', '').replace(')', '')
    if standardized_column_name not in df.columns:
        raise KeyError(f"Column '{standardized_column_name}' not found in {file_name}")
    new_col_name = f"{standardized_column_name}_{file_name.replace('.csv', '')}"
    df.rename(columns={standardized_column_name: new_col_name}, inplace=True)
    return df[[new_col_name]]

data_frames = [load_data(file, name) for file, name in independent_datasets.items()]
merged_data = reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True, how='outer'), data_frames)
merged_data.ffill(inplace=True)
merged_data.bfill(inplace=True)
merged_data.replace([np.inf, -np.inf], np.nan, inplace=True)
merged_data.dropna(inplace=True)
merged_data = merged_data.apply(pd.to_numeric, errors='coerce').dropna()
merged_data = sm.add_constant(merged_data)

# Calculate VIF for each independent variable and round to two decimals
vif_data = pd.DataFrame()
vif_data["variable"] = merged_data.columns
vif_data["VIF"] = [round(variance_inflation_factor(merged_data.values, i), 2) for i in range(merged_data.shape[1])]

print(vif_data)
vif_data.to_csv(os.path.join(results_directory, 'vif_results.csv'), index=False)
