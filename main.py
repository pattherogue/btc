import requests
import datetime
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit

# Function for hyperparameter tuning
def tune_hyperparameters(train_data):
    """
    Fine-tunes the hyperparameters of the ARIMA model using grid search.

    Args:
        train_data (pd.DataFrame): Training data for Bitcoin prices.

    Returns:
        dict: Optimal hyperparameters found through grid search.
    """
    # Convert Date column to datetime format and set as index
    train_data['Date'] = pd.to_datetime(train_data['Date'])
    train_data.set_index('Date', inplace=True)
    
    # Define parameter grid for ARIMA model
    p_values = range(0, 6)
    d_values = range(0, 3)
    q_values = range(0, 3)
    param_grid = dict(order=(p_values, d_values, q_values))
    
    # Define time series split for cross-validation
    tscv = TimeSeriesSplit(n_splits=5)
    
    # Grid search for hyperparameter tuning
    model = ARIMA(train_data['Price'], order=(5, 1, 0))  # Initial model order
    grid = GridSearchCV(estimator=model, param_grid=param_grid, scoring='neg_mean_absolute_error', cv=tscv)
    grid_result = grid.fit(train_data)
    
    # Get best hyperparameters
    best_params = grid_result.best_params_
    return best_params

# Function for cross-validation
def perform_cross_validation(model, train_data):
    """
    Performs cross-validation on the ARIMA model using time series split.

    Args:
        model (statsmodels.tsa.arima.ARIMAResultsWrapper): Trained ARIMA model.
        train_data (pd.DataFrame): Training data for Bitcoin prices.

    Returns:
        float: Mean Absolute Error (MAE) from cross-validation.
    """
    # Define time series split for cross-validation
    tscv = TimeSeriesSplit(n_splits=5)
    
    # Perform cross-validation
    mae_scores = []
    for train_index, test_index in tscv.split(train_data):
        train_split, test_split = train_data.iloc[train_index], train_data.iloc[test_index]
        arima_model = model.fit(train_split['Price'])
        predictions = arima_model.forecast(steps=len(test_split))
        mae = mean_absolute_error(test_split['Price'], predictions)
        mae_scores.append(mae)
    
    # Calculate mean MAE from cross-validation
    mean_mae = sum(mae_scores) / len(mae_scores)
    return mean_mae

# Main function
def main():
    """
    Main function to execute the program.
    """
    # Fetch Bitcoin price data
    bitcoin_data = fetch_bitcoin_data()
    
    # Preprocess the fetched data
    preprocessed_data = preprocess_data(bitcoin_data)
    
    # Split data into train and test sets
    train_data, _ = split_data(preprocessed_data)
    
    # Tune hyperparameters
    best_params = tune_hyperparameters(train_data)
    print("Best Hyperparameters:", best_params)
    
    # Train ARIMA model with best hyperparameters
    arima_model = ARIMA(train_data['Price'], order=best_params['order'])
    arima_model_fit = arima_model.fit()
    
    # Perform cross-validation
    mean_mae = perform_cross_validation(arima_model_fit, train_data)
    print("Mean MAE from Cross-Validation:", mean_mae)

if __name__ == "__main__":
    main()
