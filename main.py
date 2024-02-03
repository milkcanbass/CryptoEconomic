import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import statsmodels.api as sm

## Data Preo ##
# Load the datasets
bitC_prices = pd.read_csv("Data\BTC-USD.csv")  # Ensure the path is correct
ethC_prices = pd.read_csv("Data\ETH-USD.csv")  # Ensure the path is correct

# Convert date columns to datetime type
# Ensure the column name matches exactly with what's in your CSV files
bitC_prices['Date'] = pd.to_datetime(bitC_prices['Date'])
ethC_prices['Date'] = pd.to_datetime(ethC_prices['Date'])

# Merge the datasets on the 'Date' column
# Ensure you're merging on 'Date' if that's the corrected column name
data = pd.merge(bitC_prices, ethC_prices, on='Date', how='inner')

# Print the first few rows of the merged DataFrame
# print(data.head())
# print(bitC_prices.columns)
# print(ethC_prices.columns)

## Data Plotting ##
# Bit Coin and ETH's Historical price movement data visualization
plt.figure(figsize=(10, 5))
plt.plot(data['Date'], data['Close_x'], label='Bitcoin Price')  # Replace 'Close_BTC' with the actual column name
plt.plot(data['Date'], data['Close_y'], label='ETH Price')  # Replace 'Close_ETH' with the actual column name
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Bitcoin and Ethereum Price Over Time')
plt.legend()
plt.show()


##Linear Regression Analysis

# Define the independent variable (interest rates) and add a constant term
X = sm.add_constant(data['Close_x'])

# Define the dependent variable (Bitcoin prices)
Y = data['Close_y']

# Fit the linear regression model
model = sm.OLS(Y, X).fit()

# Print the summary of the regression
print(model.summary())

# Plot the observed data
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Close_x', y='Close_y', data=data, color='blue', alpha=0.6)

# Plot the regression line
sns.lineplot(x=data['Close_x'], y=model.predict(X), color='red')

plt.title('Linear Regression: Bitcoin Price vs. ETH Price')
plt.xlabel('Bitcoin Price')
plt.ylabel('ETH Price')
plt.show()