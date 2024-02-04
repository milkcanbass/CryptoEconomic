import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import statsmodels.api as sm
import os

## Data Preo ##
# Load the datasets
bitC_prices = pd.read_csv("Data\BTC-USD.csv")  # Ensure the path is correct
ethC_prices = pd.read_csv("Data\ETH-USD.csv")  # Ensure the path is correct
fed_rate = pd.read_csv("Data\FedRate_FRB_H15.csv", skiprows=5)

# Convert date columns to datetime type
# Ensure the column name matches exactly with what's in your CSV files
bitC_prices['Date'] = pd.to_datetime(bitC_prices['Date'])
ethC_prices['Date'] = pd.to_datetime(ethC_prices['Date'])
fed_rate["Time Period"] = pd.to_datetime(fed_rate["Time Period"])
fed_rate.rename(columns={'Time Period': 'Date', 'RIFSPFF_N.WW': 'FedRate'}, inplace=True)

# Merge the datasets on the 'Date' column
# First merge: Merge 'bitC_prices' and 'ethC_prices' on 'Date'
data_merged_once = pd.merge(bitC_prices, ethC_prices, on='Date', how='inner')
data_merged_once.rename(columns={'Close_x': 'Close_Btc'}, inplace=True)
data_merged_once.rename(columns={'Close_y': 'Close_Eth'}, inplace=True)

# Second merge: Merge the result of the first merge with 'fed_rate' on 'Date'
data = pd.merge(data_merged_once, fed_rate, on='Date', how='inner')

# Print the first few rows of the merged DataFrame
# print(data.head())
# print(bitC_prices.columns)
# print(ethC_prices.columns)

## Data Plotting ##
# Bit Coin and ETH's Historical price movement data visualization
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



# Example Usage
linear_regression_analysis(data, 'Close_Btc', 'FedRate', folder='my_folder')
plot_price_movements(data, 'Close_Btc', 'Close_Eth', label1='Bitcoin', label2='Ethereum', folder='my_folder')

