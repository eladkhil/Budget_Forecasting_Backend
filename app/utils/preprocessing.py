import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def load_and_prepare_data():
    # Example CSV loading — adapt the path and structure to your project
    df = pd.read_csv("data/budget_data.csv")  # Make sure this file exists

    # Assume columns: ['year', 'direction', 'rubrique', 'groupement', 'montant']
    # Grouping and aggregating budgets
    df_grouped = df.groupby("year")["montant"].sum().reset_index()

    # Normalize
    scaler = MinMaxScaler()
    values = scaler.fit_transform(df_grouped["montant"].values.reshape(-1, 1))

    # Create sequences for LSTM (last 10 to predict next 1)
    sequence_length = 10
    X, y = [], []

    for i in range(len(values) - sequence_length):
        X.append(values[i:i+sequence_length])
        y.append(values[i+sequence_length])

    X = np.array(X)
    y = np.array(y)

    # Simulate future input for prediction (last 10)
    X_future = values[-sequence_length:].reshape(1, sequence_length, 1)

    # Return data and labels (e.g. years)
    years = df_grouped["year"].values[-len(y):]
    future_year = df_grouped["year"].max() + 1

    return X, y, X_future, [f"{future_year} (prévision)"]
