import os
import sys
import json
import logging

import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler

from feature_binning import CustomBinningStrategy
from feature_encoding import OrdialEncodingStrategy

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from config import get_preprocessing, get_path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class ModelInference:
    """
    Loads a trained churn model and serves predictions.
    Handles the full inference path:
        - Load the model
        - Encode the data
        - Apply feature binning
        - Predict the result against the unseen data

    Args:
        model_path (str): Path to the joblib-serialized model file.
        encoder_dir (str): Directory containing encoder JSON files.
        data (dict): Single customer's raw feature values.

    Returns the prediction whether customer Churn or Retain with probability.
    """
    def __init__(self, model_path):
        self.model_path = model_path
        self.binning_config = get_preprocessing().get("feature_binning", {})
        self.encoding_config = get_preprocessing().get("encoding", {})
        self.encoders = {}
        self.scaler = None
        self.feature_columns = None
        self.load_model()

    def load_model(self):
        if not os.path.exists(self.model_path):
            raise ValueError(f"Cannot load model: file does not exist at path '{self.model_path}'")
        self.model = joblib.load(self.model_path)

    def load_encoder(self, encoder_dir):
        """
        Load per-feature encoders from a directory of JSON files.

        Each file is expected to be named "<feature_name>_encoder.json"
        and is loaded into `self.encoders[feature_name]`.
        """
        for file in os.listdir(encoder_dir):
            if not file.endswith("_encoder.json"):
                continue
            feature_name = file.replace("_encoder.json", "")
            with open(os.path.join(encoder_dir, file)) as f:
                self.encoders[feature_name] = json.load(f)

    def _resolve_path(self, path):
        if os.path.isabs(path):
            return path
        return os.path.join(ROOT_DIR, path)

    def _load_training_metadata(self):
        if self.feature_columns is not None and self.scaler is not None:
            return

        x_train_path = self._resolve_path(
            get_path().get("artifacts", {}).get("data", {}).get("X_train")
        )
        X_train = pd.read_csv(x_train_path)
        self.feature_columns = X_train.columns.tolist()

        scaling_features = get_preprocessing().get("scaling", {}).get("features", [])
        self.scaler = StandardScaler()
        self.scaler.fit(X_train[scaling_features])

    def _apply_one_hot_encoding(self, df):
        nominal_columns = self.encoding_config.get("nominal_features", [])
        for column in nominal_columns:
            dummies = pd.get_dummies(df[column], prefix=column, dtype=int)
            saved_columns = self.encoders.get(column, [])
            for col in saved_columns:
                if col not in dummies.columns:
                    dummies[col] = 0
            if saved_columns:
                dummies = dummies[saved_columns]
            df = pd.concat([df.drop(columns=[column]), dummies], axis=1)
        return df

    def preprocess_input(self, data):
        df = pd.DataFrame([data])

        for cast in get_preprocessing().get("dtype_casting", []):
            col = cast.get("column")
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        custom_binning_definition = self.binning_config.get("custom", {}).get("tenure", {})
        custom_binning = CustomBinningStrategy(custom_binning_definition)
        df = custom_binning.bin_feature(column="tenure", df=df)

        df = self._apply_one_hot_encoding(df)

        ordinal_features = self.encoding_config.get("ordinal_features", {})
        ordinal_encoding = OrdialEncodingStrategy(ordinal_features)
        df = ordinal_encoding.encode(df)

        self._load_training_metadata()
        scaling_features = get_preprocessing().get("scaling", {}).get("features", [])
        df[scaling_features] = self.scaler.transform(df[scaling_features])

        if "customerID" in df.columns:
            df = df.drop(columns=["customerID"])

        return df.reindex(columns=self.feature_columns, fill_value=0)

    def predict(self, data):
        processed_input = self.preprocess_input(data)
        Y_pred = self.model.predict(processed_input)
        Y_proba = float(self.model.predict_proba(processed_input)[0, 1])

        Y_pred = "Churn" if Y_pred == 1 else "Retain"
        Y_proba = round(Y_proba * 100, 2)

        return {
            "Status": Y_pred,
            "Confidence": f"{Y_proba}%"
        }
