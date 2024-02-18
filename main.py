import requests
import datetime
import matplotlib.pyplot as plt
import pandas as pd

# Function for fetching Bitcoin data
def fetch_bitcoin_data():
    """
    Fetches historical Bitcoin price data from the CoinGecko API.

    Returns:
        dict: Bitcoin price data in JSON format.
    """
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': '365',  # Fetch data for the last year
        'interval': 'daily'
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

# Function for preprocessing Bitcoin data
def preprocess_data(data):
    """
    Preprocesses the fetched Bitcoin price data.

    Args:
        data (dict): Bitcoin price data in JSON format.

    Returns:
        pd.DataFrame: Preprocessed Bitcoin price data.
    """
 # Extract timestamps and prices from the data dictionary
    timestamps = [ts for ts, _ in data['prices']]
    prices = [price for _, price in data['prices']]
    
    # Convert timestamps to datetime objects
    dates = [datetime.datetime.fromtimestamp(ts / 1000).strftime('%Y-%m-%d') for ts in timestamps]
    
    # Create DataFrame
    df = pd.DataFrame({'Date': dates, 'Price': prices})
    return df


# Function for visualizing Bitcoin price data over time
def visualize_bitcoin_price(data):
    """
    Visualizes the Bitcoin price over time.

    Args:
        data (pd.DataFrame): Bitcoin price data in DataFrame format.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(data['Date'], data['Price'], color='blue', marker='o', linestyle='-')
    plt.title('Bitcoin Price Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Function for calculating basic statistics of Bitcoin prices
def calculate_basic_statistics(data):
    """
    Calculates basic statistics of Bitcoin prices.

    Args:
        data (pd.DataFrame): Bitcoin price data in DataFrame format.

    Prints:
        Basic statistics such as mean, median, minimum, and maximum prices.
    """
    mean_price = data['Price'].mean()
    median_price = data['Price'].median()
    min_price = data['Price'].min()
    max_price = data['Price'].max()
    
    print("Basic Statistics:")
    print(f"Mean Price: {mean_price:.2f} USD")
    print(f"Median Price: {median_price:.2f} USD")
    print(f"Minimum Price: {min_price:.2f} USD")
    print(f"Maximum Price: {max_price:.2f} USD")

# Main function
def main():
    """
    Main function to execute the program.
    """
    # Fetch Bitcoin price data
    bitcoin_data = fetch_bitcoin_data()
    
    # Preprocess the fetched data
    preprocessed_data = preprocess_data(bitcoin_data)
    
    # Calculate basic statistics
    calculate_basic_statistics(preprocessed_data)
    
    # Visualize Bitcoin price over time
    visualize_bitcoin_price(preprocessed_data)
    
if __name__ == "__main__":
    main()
