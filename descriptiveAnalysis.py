import pandas as pd
import os

def read_and_describe(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    all_stats = []

    for file in files:
        file_path = os.path.join(directory, file)
        df = pd.read_csv(file_path)

        # Standardize column names: remove spaces and special characters for easier matching
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '').str.replace('.', '').str.replace('*', '').str.replace(',', '')

        # Identify the data structure and select the target column for descriptive analysis
        if 'close' in df.columns and 'adjclose' in df.columns:
            target_col = 'close'
        elif len(df.columns) == 2:  # Assuming the second column is the target if there are only two columns
            target_col = df.columns[1]
            # Convert to numeric, coercing errors
            df[target_col] = pd.to_numeric(df[target_col], errors='coerce')
        elif 'price' in df.columns:
            target_col = 'price'
        elif 'close' in df.columns:
            target_col = 'close'
        else:
            print(f"Unknown structure for {file}, skipping.")
            continue

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
        print(f"Check if the file is open elsewhere or the permissions of the folder: {file_path}")

directory = 'Data'
try:
    descriptive_stats = read_and_describe(directory)
    if not descriptive_stats.empty:
        save_to_csv(descriptive_stats, directory)
    else:
        print("No descriptive statistics were generated.")
except Exception as e:
    print(f"An error occurred during the processing: {e}")
