import pandas as pd
import statsmodels.api as sm
import os

def load_and_prepare_data(file_name, column_name, directory='Data'):
    df = pd.read_csv(os.path.join(directory, file_name), parse_dates=['DATE'])
    df.set_index('DATE', inplace=True)
    
    # Ensure we are using the correct column name
    if 'Close*' in file_name:
        column_name = 'Close*'
    if column_name not in df.columns:
        print(f"Warning: Column {column_name} not found in {file_name}. Columns available: {df.columns}")
        return pd.DataFrame()  # return an empty DataFrame if the column is not found

    # Prepare the DataFrame by renaming the column to include the file name
    new_column_name = f"{file_name[:-4]}_{column_name.replace('*', '')}"
    df.rename(columns={column_name: new_column_name}, inplace=True)
    return df[[new_column_name]]

data_directory = 'Data'
btc_data = load_and_prepare_data('BTC-USD.csv', 'Close', data_directory)

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

for file_name, column_name in datasets.items():
    df = load_and_prepare_data(file_name, column_name, data_directory)
    if not df.empty:
        btc_data = btc_data.join(df, how='outer', rsuffix='_other')  # Add a suffix to avoid column name clashes

# Forward fill to handle any NaN values from non-daily data
btc_data.ffill(inplace=True)

# Ensure all data is numeric and drop any remaining NaNs
btc_data = btc_data.apply(pd.to_numeric, errors='coerce').dropna()

if not btc_data.empty:
    X = btc_data.drop('BTC-USD_Close', axis=1, errors='ignore')
    y = btc_data['BTC-USD_Close']
    X = sm.add_constant(X)  # Adding a constant column for intercept
    model = sm.OLS(y, X, missing='drop')
    results = model.fit()
    print(results.summary())
else:
    print("Error: No data available for regression.")
