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
        dict: Preprocessed Bitcoin price data.
    """
    # Handle missing values
    # (Assuming missing values are not present in the current data)
    
    # Address outliers
    # (You may need to perform outlier detection and decide how to handle outliers)
    
    # Ensure consistency
    # (Check for inconsistencies such as inconsistent formatting or data types)
    
    # Normalize data
    # (You may need to scale or normalize the data, depending on the algorithms used)
    
    # Convert timestamps to human-readable dates
    for data_point in data['prices']:
        timestamp = data_point[0] / 1000  # Convert milliseconds to seconds
        date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        data_point[0] = date
    return data

# Function for visualizing Bitcoin price data over time
def visualize_bitcoin_price(data):
    """
    Visualizes the Bitcoin price over time.

    Args:
        data (dict): Bitcoin price data in JSON format.
    """
    dates = [data_point[0] for data_point in data['prices']]
    prices = [data_point[1] for data_point in data['prices']]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, prices, color='blue', marker='o', linestyle='-')
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
        data (dict): Bitcoin price data in JSON format.

    Prints:
        Basic statistics such as mean, median, minimum, and maximum prices.
    """
    prices = [data_point[1] for data_point in data['prices']]
    mean_price = sum(prices) / len(prices)
    median_price = sorted(prices)[len(prices) // 2]
    min_price = min(prices)
    max_price = max(prices)
    
    print("Basic Statistics:")
    print(f"Mean Price: {mean_price:.2f} USD")
    print(f"Median Price: {median_price:.2f} USD")
    print(f"Minimum Price: {min_price:.2f} USD")
    print(f"Maximum Price: {max_price:.2f} USD")

# Function for performing time series analysis
def perform_time_series_analysis(data):
    """
    Performs time series analysis on Bitcoin price data.

    Args:
        data (dict): Bitcoin price data in JSON format.
    """
    try:
        # Convert 'Date' column to datetime format
        df = pd.DataFrame(data['prices'], columns=['Date', 'Price'])
        print("Before Conversion:")
        print(df['Date'].head())  # Debugging statement
        df['Date'] = pd.to_datetime(df['Date'], errors='raise', unit='ms')
        print("After Conversion:")
        print(df['Date'].head())  # Debugging statement

        # Add your time series analysis code here
        
    except Exception as e:
        print(f"Error occurred during time series analysis: {e}")

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
    
    # Perform time series analysis
    perform_time_series_analysis(preprocessed_data)
    
if __name__ == "__main__":
    main()
