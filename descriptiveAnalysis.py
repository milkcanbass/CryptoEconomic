import pandas as pd
import os

def read_and_describe(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    all_stats = []

    for file in files:
        file_path = os.path.join(directory, file)
        df = pd.read_csv(file_path)

        # Standardize column names and clean them
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '').str.replace('.', '').str.replace('*', '').str.replace(',', '')

        # Determine the target column and ensure it is the correct type
        if 'close' in df.columns and 'adjclose' in df.columns:
            target_col = 'close'
        elif len(df.columns) == 2:  # Assuming second column is the data column
            target_col = df.columns[1]
            # Try to convert to numeric, handling non-numeric data
            df[target_col] = pd.to_numeric(df[target_col], errors='coerce')
        elif 'price' in df.columns:
            target_col = 'price'
        elif 'close' in df.columns:
            target_col = 'close'
        else:
            print(f"Unknown structure for {file}, skipping.")
            continue

        # Calculate descriptive statistics
        stats = df[target_col].describe(include='all')  # Include all types of data
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
    df.to_csv(os.path.join(result_directory, filename))
    print(f"Descriptive statistics saved to {os.path.join(result_directory, filename)}")

directory = 'Data'
descriptive_stats = read_and_describe(directory)
if not descriptive_stats.empty:
    save_to_csv(descriptive_stats, directory)
else:
    print("No descriptive statistics were generated.")
