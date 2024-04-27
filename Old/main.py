import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import statsmodels.api as sm
import os

## Data Prep ##

# Load the datasets
bitC_prices = pd.read_csv("Data/BTC-USD.csv", parse_dates=['Date'])
ethC_prices = pd.read_csv("Data/ETH-USD.csv", parse_dates=['Date'])
fed_rate = pd.read_csv("Data/FedRate_FRB_H15.csv", skiprows=5, parse_dates=["Time Period"])
fed_rate.rename(columns={'Time Period': 'Date', 'RIFSPFF_N.WW': 'FedRate'}, inplace=True)

personal_savings = pd.read_csv("Data/Personal Saving rate.csv")
personal_savings['Date'] = pd.to_datetime(personal_savings['DATE'])  # Adjust 'DATE' if your column name differs
personal_savings.drop(columns=['DATE'], inplace=True)  # Drop the original 'DATE' column
personal_savings.set_index('Date', inplace=True)
personal_savings_daily = personal_savings.resample('D').ffill()
personal_savings_daily.reset_index(inplace=True)

# Specify the renaming of columns after merging
rename_dict = {
    'Close_x': 'Close_Btc',
    'Close_y': 'Close_Eth'
}

# Merge task
def merge_data(dataframes, on='Date', how='inner', rename_cols=None):
    merged_data = dataframes[0]
    for df in dataframes[1:]:
        merged_data = pd.merge(merged_data, df, on=on, how=how)
        if rename_cols:
            merged_data.rename(columns=rename_cols, inplace=True)
    return merged_data

# Merge all datasets on the 'Date' column with column renaming
data = merge_data([bitC_prices, ethC_prices, fed_rate, personal_savings_daily], rename_cols=rename_dict)

## Functions ##
# Data plotting
def plot_price_movements(data, col1, col2, label1='First Asset', label2='Second Asset', folder='results', filename='price_movements.png'):
    os.makedirs(folder, exist_ok=True)
    plot_file_path = os.path.join(folder, filename)
    plt.figure(figsize=(10, 5))
    plt.plot(data['Date'], data[col1], label=label1)
    plt.plot(data['Date'], data[col2], label=label2)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'{label1} and {label2} Price Over Time')
    plt.legend()
    plt.savefig(plot_file_path)
    plt.show()

## Linear Regression Analysis
def linear_regression_analysis(data, independent_col, dependent_col, plot=True, folder='results', plot_filename='linear_regression.png', summary_filename='regression_summary.png'):
    X = sm.add_constant(data[independent_col])
    Y = data[dependent_col]
    model = sm.OLS(Y, X).fit()
    print(model.summary())
    os.makedirs(folder, exist_ok=True)
    summary_image_path = os.path.join(folder, summary_filename)
    plot_image_path = os.path.join(folder, plot_filename)
    summary_str = str(model.summary())
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.text(0.01, 0.99, summary_str, verticalalignment='top', horizontalalignment='left', family='monospace', fontsize=10, transform=ax.transAxes)
    ax.axis('off')
    plt.savefig(summary_image_path, bbox_inches='tight')
    plt.close(fig)
    if plot:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=independent_col, y=dependent_col, data=data, color='blue', alpha=0.6)
        sns.lineplot(x=data[independent_col], y=model.predict(X), color='red')
        plt.title(f'Linear Regression: {dependent_col} vs. {independent_col}')
        plt.xlabel(independent_col)
        plt.ylabel(dependent_col)
        plt.savefig(plot_image_path)
        plt.show()

def linear_reg_plot_price_mov(independent_col, dependent_col, folder, indxDep_name):
    linear_regression_analysis(data, independent_col, dependent_col, folder=folder, plot_filename=f'{indxDep_name}_linear_regression.png', summary_filename=f'{indxDep_name}_regression_summary.png')
    plot_price_movements(data, independent_col, dependent_col, label1=independent_col, label2=dependent_col, folder=folder, filename=f'{indxDep_name}_price_movements.png')




## Use functions
# #Fed Rate vs BTC Price
linear_reg_plot_price_mov(independent_col='FedRate', dependent_col='Close_Btc', folder='my_folder', indxDep_name='FedRatexBTC')

# # #BTC Price vs BTC Price
# linear_reg_plot_price_mov(independent_col='Close_Btc', dependent_col='Close_Eth', folder='my_folder', indxDep_name='BTCxETH')

# #Saving Rate vs BTC Price
# linear_reg_plot_price_mov(independent_col='PSAVERT', dependent_col='Close_Btc', folder='my_folder', indxDep_name='PersonalSavingxBTC')

