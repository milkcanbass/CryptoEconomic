import pandas as pd
import statsmodels.api as sm
import os

def load_data(file_name, column_name, directory='Data'):
    df = pd.read_csv(os.path.join(directory, file_name))
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    df = df.dropna(subset=['DATE'])
    df.set_index('DATE', inplace=True)
    return df.rename(columns={column_name: file_name.split('.')[0]})

def resample_data(df, freq='D'):
    if freq == 'M':
        freq = 'ME'
    elif freq == 'Q':
        freq = 'QE'
    return df.resample(freq).last()

# Load BTC-USD as the dependent variable
btc_data = load_data('BTC-USD.csv', 'Close')

# Dictionary of independent variables with their file names and target columns
variables = {
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
    'GSPC - S&P 500.csv': 'Close',
    'UNRATE.csv': 'UNRATE',
    'USSTHPI.csv': 'USSTHPI',
    'WM2NS.csv': 'WM2NS'
}

# Load and resample each independent variable
for file_name, column_name in variables.items():
    df = load_data(file_name, column_name)
    if 'monthly' in file_name.lower():
        df = resample_data(df, 'ME')
    elif 'quarterly' in file_name.lower():
        df = resample_data(df, 'QE')
    elif 'weekly' in file_name.lower():
        df = resample_data(df, 'W')
    btc_data = btc_data.join(df, how='left', rsuffix=f'_{file_name.split(".")[0]}')

print("Columns available in btc_data:", btc_data.columns)
if 'Close' in btc_data.columns:
    X = btc_data.drop('Close', axis=1)
    X = sm.add_constant(X)  # adding a constant
    y = btc_data['Close']

    # Perform OLS regression
    model = sm.OLS(y, X)
    results = model.fit()

    # Print and save the results
    print(results.summary())
    result_path = os.path.join('Data', 'Result', 'regression_results.csv')
    results.summary2().tables[1].to_csv(result_path)
    print(f'Regression results saved to {result_path}')
else:
    print("Error: 'Close' column not found in btc_data.")


# Prepare data for regression
btc_data = btc_data.dropna()
X = btc_data.drop('Close', axis=1)
X = sm.add_constant(X)  # adding a constant
y = btc_data['Close']

# Perform OLS regression
model = sm.OLS(y, X)
results = model.fit()

# Print the results
print(results.summary())

# Save the regression results to a CSV file
result_path = os.path.join('Data', 'Result', 'regression_results.csv')
results_summary = results.summary2().tables[1]
results_summary.to_csv(result_path)
print(f'Regression results saved to {result_path}')
