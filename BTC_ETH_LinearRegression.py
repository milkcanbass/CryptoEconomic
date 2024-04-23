import pandas as pd
import statsmodels.api as sm
import os

def load_and_prepare_data(file_path):
    df = pd.read_csv(file_path)
    df['DATE'] = pd.to_datetime(df['DATE'])
    df.set_index('DATE', inplace=True)
    return df

def perform_linear_regression(df):
    # Adding a constant for the intercept term in the regression model
    X = sm.add_constant(df.index.to_julian_date())  # Using Julian date for regression
    y = df['Close']
    model = sm.OLS(y, X)
    results = model.fit()
    return results

def save_regression_results(results, directory, filename):
    summary = results.summary()
    with open(os.path.join(directory, filename), 'w') as f:
        f.write(summary.as_text())

# Directory setup
data_directory = 'Data'
result_directory = os.path.join(data_directory, 'Result')
if not os.path.exists(result_directory):
    os.makedirs(result_directory)

# File names
files = ['BTC-USD.csv', 'BTC-USD.csv']  # Assuming two different files

# Process each file
for file_name in files:
    file_path = os.path.join(data_directory, file_name)
    df = load_and_prepare_data(file_path)
    results = perform_linear_regression(df)
    result_filename = f"linear_regression_{file_name.replace('.csv', '')}.txt"  # Saving as .txt for readability
    save_regression_results(results, result_directory, result_filename)
