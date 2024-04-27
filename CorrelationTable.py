import pandas as pd
import os
from functools import reduce
import seaborn as sns
import matplotlib.pyplot as plt


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
    'ETH-USD.csv': 'Close',
    'BTC-USD.csv': 'Close'
}

data_directory = 'Data'  # Define the directory where your CSV files are stored

# Load and prepare data
all_data = []
for file_name, column_name in datasets.items():
    file_path = os.path.join(data_directory, file_name)
    df = pd.read_csv(file_path)
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    df.dropna(subset=['DATE'], inplace=True)
    df.set_index('DATE', inplace=True)
    df = df[[column_name]].rename(columns={column_name: column_name + '_' + file_name.split('.')[0]})
    df = df.apply(pd.to_numeric, errors='coerce')
    all_data.append(df)

# Merge using outer join and fill missing data with forward fill
merged_data = reduce(lambda left, right: pd.merge(left, right, on='DATE', how='outer'), all_data)
merged_data.fillna(method='ffill', inplace=True)  # Forward fill to handle NaNs

# Calculate correlations
correlation_matrix = merged_data.corr()

# Print and save the correlation matrix
print(correlation_matrix)
correlation_matrix.to_csv(os.path.join(data_directory, 'correlation_matrix.csv'))

# Print the DataFrame after merging and cleaning for inspection
print(merged_data.head())

#heat map
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix')
plt.show()