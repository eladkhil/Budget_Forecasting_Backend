from app.utils.preprocessing import load_and_prepare_data
from app.models.lstm_model import LSTMModel
import numpy as np

def run_prediction_pipeline():
    # 1. Load and preprocess the data
    X_train, y_train, X_future, labels = load_and_prepare_data()

    # 2. Initialize and train the model
    model = LSTMModel(input_shape=(X_train.shape[1], X_train.shape[2]))
    model.train(X_train, y_train)

    # 3. Predict future budgets
    predictions = model.predict(X_future)

    # 4. Build the report
    report = []
    for i in range(len(predictions)):
        report.append({
            "label": labels[i],
            "predicted_budget": round(float(predictions[i][0]), 2)
        })

    return {"future_budgets": report}
