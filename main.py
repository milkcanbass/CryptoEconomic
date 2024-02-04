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
personal_savings = pd.read_csv("Data/Personal Saving rate.csv", parse_dates=['DATE'])  # Assuming 'Date' column exists
personal_savings.rename(columns={'DATE':'Date'}, inplace=True)
# Specify the renaming of columns after merging
rename_dict = {
    'Close_x': 'Close_Btc',
    'Close_y': 'Close_Eth'
}

btc_dates = set(bitC_prices['Date'])
eth_dates = set(ethC_prices['Date'])
fed_dates = set(fed_rate['Date'])
savings_dates = set(personal_savings['Date'])

# Find common dates
common_dates = btc_dates.intersection(eth_dates, fed_dates, savings_dates)
print(f"Number of common dates: {len(common_dates)}")



# merge task
def merge_data(dataframes, on='Date', how='inner', rename_cols=None):
    # Initialize merged data with the first dataframe
    merged_data = dataframes[0]

    # Iterate over the remaining dataframes and merge them one by one
    for df in dataframes[1:]:
        merged_data = pd.merge(merged_data, df, on=on, how=how)

        # Rename columns if rename_cols is specified
        if rename_cols:
            merged_data.rename(columns=rename_cols, inplace=True)

    return merged_data


# Merge all datasets on the 'Date' column with column renaming
data = merge_data([bitC_prices, ethC_prices, fed_rate, personal_savings], rename_cols=rename_dict)

# Check the resulting DataFrame
print(data.head())




## Functions ##
# Data plotting 
def plot_price_movements(data, col1, col2, label1='First Asset', label2='Second Asset', folder='results', filename='price_movements.png'):
    # Ensure the folder exists
    os.makedirs(folder, exist_ok=True)

    # Full path for the plot image file
    plot_file_path = os.path.join(folder, filename)

    plt.figure(figsize=(10, 5))
    plt.plot(data['Date'], data[col1], label=label1)
    plt.plot(data['Date'], data[col2], label=label2)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'{label1} and {label2} Price Over Time')
    plt.legend()
    
    # Save the figure as an image file in the specified folder before showing it
    plt.savefig(plot_file_path)
    plt.show()




##Linear Regression Analysis
def linear_regression_analysis(data, independent_col, dependent_col, plot=True, folder='results', plot_filename='linear_regression.png', summary_filename='regression_summary.png'):
    # Define the independent variable (X) and add a constant term
    X = sm.add_constant(data[independent_col])
    Y = data[dependent_col]  # Define the dependent variable (Y)
    model = sm.OLS(Y, X).fit()  # Fit the linear regression model
    print(model.summary())  # Print the summary of the regression

    # Ensure the folder exists
    os.makedirs(folder, exist_ok=True)

    # Full path for the summary image file and plot image file
    summary_image_path = os.path.join(folder, summary_filename)
    plot_image_path = os.path.join(folder, plot_filename)

    # Convert the summary to a string
    summary_str = str(model.summary())

    # Create a figure and add text of the summary to it
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.text(0.01, 0.99, summary_str, verticalalignment='top', horizontalalignment='left', family='monospace', fontsize=10, transform=ax.transAxes)
    ax.axis('off')

    # Save the figure containing the summary text as an image
    plt.savefig(summary_image_path, bbox_inches='tight')
    plt.close(fig)  # Close the figure to prevent it from displaying

    if plot:
        # Plot the observed data
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=independent_col, y=dependent_col, data=data, color='blue', alpha=0.6)

        # Plot the regression line
        sns.lineplot(x=data[independent_col], y=model.predict(X), color='red')

        plt.title(f'Linear Regression: {dependent_col} vs. {independent_col}')
        plt.xlabel(independent_col)
        plt.ylabel(dependent_col)
        
        # Save the plot image in the specified folder
        plt.savefig(plot_image_path)
        plt.show()

def linear_reg_plot_price_mov(independent_col, dependent_col, folder, indxDep_name):
    linear_regression_analysis(data, independent_col,dependent_col,folder=folder,  plot_filename=f'{indxDep_name}_linear_regression.png',summary_filename= f'{indxDep_name}_regression_summary.png')
    plot_price_movements(data, independent_col,dependent_col, label1=independent_col, label2=dependent_col, folder=folder, filename=f'{indxDep_name}_price_movements.png')



## Use functions
# #Fed Rate vs BTC Price
# linear_reg_plot_price_mov(independent_col='FedRate', dependent_col='Close_Btc', folder='my_folder', indxDep_name='FedRatexBTC')

# #BTC Price vs BTC Price
# linear_reg_plot_price_mov(independent_col='Close_Btc', dependent_col='Close_Eth', folder='my_folder', indxDep_name='BTCxETH')

# #Saving Rate vs BTC Price
# linear_reg_plot_price_mov(independent_col='Close_Btc', dependent_col='Close_Eth', folder='my_folder', indxDep_name='BTCxETH')

