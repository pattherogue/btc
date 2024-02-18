import requests
import datetime
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import TimeSeriesSplit
from statsmodels.tsa.api import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA

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

# Function for model selection and evaluation
def select_and_evaluate_model(data):
    """
    Selects and evaluates models for time series forecasting.

    Args:
        data (pd.DataFrame): Preprocessed Bitcoin price data.

    Returns:
        dict: Evaluation results for each model.
    """
    evaluation_results = {}

    # Split data for time series cross-validation
    tscv = TimeSeriesSplit(n_splits=5)

    # Define models
    models = [
        ('Exponential Smoothing', ExponentialSmoothing),
        ('ARIMA', ARIMA)
    ]

    for model_name, model_class in models:
        print(f"Evaluating {model_name}...")
        mae_scores = []
        for train_index, test_index in tscv.split(data):
            train_data = data.iloc[train_index]
            test_data = data.iloc[test_index]

            # Fit model
            model = model_class(train_data['Price'])
            model_fit = model.fit()

            # Make predictions
            forecast = model_fit.forecast(len(test_data))

            # Calculate MAE
            mae = mean_absolute_error(test_data['Price'], forecast)
            mae_scores.append(mae)

        evaluation_results[model_name] = mae_scores

    return evaluation_results

# Function for visualizing model evaluation results
def visualize_evaluation_results(evaluation_results):
    """
    Visualizes the evaluation results for different models.

    Args:
        evaluation_results (dict): Evaluation results for each model.
    """
    plt.figure(figsize=(10, 6))
    for model_name, scores in evaluation_results.items():
        plt.plot(range(1, len(scores) + 1), scores, label=model_name)
    plt.title('Model Evaluation Results')
    plt.xlabel('Fold')
    plt.ylabel('Mean Absolute Error')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Main function
def main():
    """
    Main function to execute the program.
    """
    # Fetch Bitcoin price data
    bitcoin_data = fetch_bitcoin_data()
    
    # Preprocess the fetched data
    preprocessed_data = preprocess_data(bitcoin_data)

    # Select and evaluate models
    evaluation_results = select_and_evaluate_model(preprocessed_data)
    
    # Visualize model evaluation results
    visualize_evaluation_results(evaluation_results)

if __name__ == "__main__":
    main()
