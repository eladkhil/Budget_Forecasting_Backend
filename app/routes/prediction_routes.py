from flask import Blueprint, request, jsonify
from app.services.prediction_service import run_prediction_pipeline


bp_prediction = Blueprint("bp_prediction", __name__, url_prefix="/api/predict")

@bp_prediction.route("/future-budgets", methods=["POST"])

def predict_future_budgets():
    try:
        report = run_prediction_pipeline()
        return jsonify(report), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500