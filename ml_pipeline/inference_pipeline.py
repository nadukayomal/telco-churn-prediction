import json
import sys
import os
import logging
import joblib
from typing import Dict, Any, Tuple, Optional
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from config import get_path
from model_inference import ModelInference
logging.basicConfig(
                    level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    )
logger = logging.getLogger(__name__)

""" Define config """
encode_path = get_path().get("artifacts", {})["encode"]
model_path = get_path().get("model", {})["model_path"]

# Calling inference class
inference = ModelInference(model_path)

def streaming_inference(inference, data):
    inference.load_encoder(encode_path)
    pred = inference.predict(data)
    return pred

if __name__ == "__main__":
    data = {
            "customerID": "4821-KLQMN",
            "gender": "Male",
            "SeniorCitizen": 1,
            "Partner": "No",
            "Dependents": "No",
            "tenure": 8,
            "PhoneService": "Yes",
            "MultipleLines": "Yes",
            "InternetService": "Fiber optic",
            "OnlineSecurity": "No",
            "OnlineBackup": "Yes",
            "DeviceProtection": "Yes",
            "TechSupport": "No",
            "StreamingTV": "Yes",
            "StreamingMovies": "Yes",
            "Contract": "Month-to-month",
            "PaperlessBilling": "Yes",
            "PaymentMethod": "Electronic check",
            "MonthlyCharges": 94.65,
            "TotalCharges": 757.20
        }

    pred = streaming_inference(inference, data)
    print(pred)

