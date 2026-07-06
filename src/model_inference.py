from nt import error
from shlex import join
import os, sys
import json
from tkinter import Y
import joblib
import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, Optional

from pandas.io.xml import preprocess_data

from feature_binning import CustomBinningStrategy, BinaryBinnig
from feature_encoding import OrdialEncodingStrategy, NominalEncodingStrategy

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from config import get_preprocessing
logging.basicConfig(
                    level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    )
logger = logging.getLogger(__name__)



class ModelInference:
    """
    Loads a trained churn model and serves predictions.
    Handles the full inference path:
        - Load the model
        - Encode the data
        - Apply feature binning
        - Predict the result againts the unseen data

    Args :
        model_path (str): Path to the joblib-serialized model file.
        ncoder_dir (str): Directory containing encoder JSON files.
        data (dict): Single customer's raw feature values.

    Return the prediction is customer Churn or Retain with probability
    
    """
    def __init__(self, model_path):
        self.model_path = model_path
        self.binning_config = get_preprocessing().get("feature_binning", {})
        self.encoding_config = get_preprocessing().get("encoding", {})
        self.encoders = {}
        self.load_model()

    def load_model(self):
        if not os.path.exists(self.model_path):
            raise ValueError(f"Cannot load model: file does not exist at path '{self.model_path}'")
        self.model = joblib.load(self.model_path)

    def load_encoder(self, encoder_dir):
        for file in os.listdir(encoder_dir):
            feature_name = file.split('_encoder.json')[0]
            with open(os.path.join(encoder_dir, file)) as f:
                self.encoders[feature_name] = join.load(f)

    def preprocess_input(self, data):
        df = pd.DataFrame([data])
        binnig_features = get_preprocessing().get("feature_binning", {})
        encoding_features = get_preprocessing().get("encoding", {})

        for col, encoder in self.encoders.items():
            df[col] = df[col].map(encoder)
        
        #  Preproces input data in feature binning calling feature binning class
        custom_binning = CustomBinningStrategy(binnig_features.get("tenure", {})) 
        binary_binning = BinaryBinnig(binnig_features.get("churn", {}))
        #  Apply binning data into the inputed Data Frame 
        df = custom_binning.bin_feature(df, 'tenure')
        df = binary_binning.bin_feature(df, 'churn')
        #  Preprocess data calling feature encoding class
        ordinal_encoding = OrdialEncodingStrategy(encoding_features.get("ordinal_features", {}))
        nominal_encoding = NominalEncodingStrategy(encoding_features.get("nominal_features", {})) 
        #  Apply encoding data into inputed Data Frame
        df = ordinal_encoding.encode(df)
        df = nominal_encoding.encode(df)
        #  Drop the unnecessary columns
        df = df.drop(columns = ["customerID"])

        return df
    
    def predict(self, data):
        processed_input = self.preprocess_input(data)
        Y_pred = self.model.predict(processed_input)
        Y_proba = float(self.model.predict_proba(processed_input)[0,1])

        Y_pred = "Churn" if Y_pred == 1 else "Retain"
        Y_proba = round(Y_proba * 100,2)

        return {
                "Status" : Y_pred,
                "Confidence" : f"{Y_proba}%"
                }

