import pandas as pd
import statsmodels.api as sm
import numpy as np
import os

def load_data(file_name, column_name, new_column_name, directory='Data'):
    file_path = os.path.join(directory, file_name)
    df = pd.read_csv(file_path, parse_dates=['DATE'])
    df.set_index('DATE', inplace=True)
    df = df[[column_name]].rename(columns={column_name: new_column_name})
    df[new_column_name] = pd.to_numeric(df[new_column_name], errors='coerce')  # Convert to numeric, coerce errors
    return df

# Define directory
data_directory = 'Data'

# Load and prepare data
btc_data = load_data('BTC-USD.csv', 'Close', 'BTC_Close')
vix_data = load_data('^VIX.csv', 'Close', 'VIX_Close')
ixic_data = load_data('^IXIC.csv', 'Close', 'IXIC_Close')
crude_data = load_data('Crude Oil.csv', 'Price', 'Crude_Price')
dgs2_data = load_data('DGS2.csv', 'DGS2', 'DGS2')
dgs5_data = load_data('DGS5.csv', 'DGS5', 'DGS5')
dgs10_data = load_data('DGS10.csv', 'DGS10', 'DGS10')
dgs30_data = load_data('DGS30.csv', 'DGS30', 'DGS30')
dji_data = load_data('DJI.csv', 'Close*', 'DJI_Close')
gold_data = load_data('Gold.csv', 'Price', 'Gold_Price')
gspc_data = load_data('GSPC - S&P 500.csv', 'Close*', 'GSPC_Close')

# Join all dataframes
data_frames = [vix_data, ixic_data, crude_data, dgs2_data, dgs5_data,
               dgs10_data, dgs30_data, dji_data, gold_data, gspc_data]
btc_data = btc_data.join(data_frames, how='outer')

# Forward fill and drop NaNs
btc_data.ffill(inplace=True)
btc_data.dropna(inplace=True)

# Ensure all data is numeric
btc_data = btc_data.apply(pd.to_numeric, errors='coerce')
btc_data.dropna(inplace=True)  # Drop any rows that still contain NaN

if not btc_data.empty:
    X = btc_data.drop('BTC_Close', axis=1)
    y = btc_data['BTC_Close']
    X = sm.add_constant(X)  # adding a constant column for intercept
    model = sm.OLS(y, X, missing='drop')
    results = model.fit()
    print(results.summary())
else:
    print("Error: No data available for regression after cleaning.")
