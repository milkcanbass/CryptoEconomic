import pandas as pd
import statsmodels.api as sm
import numpy as np
import os

def load_and_prepare_data(file_name, column_name, frequency, directory='Data', base_index=None):
    df = pd.read_csv(os.path.join(directory, file_name), parse_dates=['DATE'])
    df.set_index('DATE', inplace=True)
    if frequency != 'D':
        df = df.resample('D').ffill().reindex(base_index).ffill().bfill()
    df = df[[column_name]] if column_name in df.columns else df[[column_name + '*']]
    df.rename(columns={column_name: f"{file_name[:-4]}_{column_name}"}, inplace=True)
    return df

data_directory = 'Data'
btc_data = load_and_prepare_data('BTC-USD.csv', 'Close', 'D', data_directory)
base_index = btc_data.index  # Base index from BTC data

datasets = {
    '^IXIC.csv': ('Close', 'D'),
    '^VIX.csv': ('Close', 'D'),
    'BOGMBASE.csv': ('BOGMBASE', 'M'),
    'CPIAUCSL.csv': ('CPIAUCSL', 'M'),
    'Crude Oil.csv': ('Price', 'D'),
    'DGS2.csv': ('DGS2', 'D'),
    'DGS5.csv': ('DGS5', 'D'),
    'DGS10.csv': ('DGS10', 'D'),
    'DGS30.csv': ('DGS30', 'D'),
    'DJI.csv': ('Close*', 'D'),
    'FEDFUNDS.csv': ('FEDFUNDS', 'M'),
    'Gold.csv': ('Price', 'D'),
    'GSPC - S&P 500.csv': ('Close*', 'D'),
    'UNRATE.csv': ('UNRATE', 'M'),
    'USSTHPI.csv': ('USSTHPI', 'Q'),
    'WM2NS.csv': ('WM2NS', 'W')
}

for file_name, (column_name, freq) in datasets.items():
    df = load_and_prepare_data(file_name, column_name, freq, data_directory, base_index)
    before_join = btc_data.dropna().shape[0]
    btc_data = btc_data.join(df, how='left')
    after_join = btc_data.dropna().shape[0]
    print(f"After joining {file_name}: Before = {before_join}, After = {after_join}")

btc_data.ffill(inplace=True)
btc_data.dropna(inplace=True)

if btc_data.empty:
    print("Error: Data is empty after joining and cleaning.")
else:
    X = btc_data.drop('BTC-USD_Close', axis=1)
    X = sm.add_constant(X)
    y = btc_data['BTC-USD_Close']

    model = sm.OLS(y, X, missing='drop')
    results = model.fit()
    print(results.summary())

