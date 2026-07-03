from enum import unique
import json
import logging
import os
import pandas as pd
import numpy as np

from typing import Dict, List, Mapping
from abc import ABC, abstractmethod
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class FeatureEncodingStrategy(ABC):
    @abstractmethod
    def encode(self, df: pd.DataFrame):
        pass

class NominalEncodingStrategy(FeatureEncodingStrategy):
    def __init__(self, nominal_columns):
        self.nominal_columns = nominal_columns
        self.encoder_dicts = {}
        os.makedirs("artifacts/encode", exist_ok=True)

    def encode(self, df):
        for column in self.nominal_columns:
            unique_values = df[column].unique()
            encoder_dict = {value : i for i, value in enumerate(unique_values)}
            self.encoder_dicts[column] = encoder_dict

            encoder_path = os.path.join("artifacts/encode", f"{column}_encoder.json")
            with open(encoder_path, "w") as f:
                json.dump(encoder_dict, f)
            
            df[column] = df[column].map(encoder_dict)
            logging.INFO(f"Encoded the feature {column} create file {column}_encoder.json")
        return df

    def get_encoder_dicts(self):
        return self.encoder_dicts


class OrdialEncodingStrategy(FeatureEncodingStrategy):
    def __init__(self, ordinal_columns):
        self.ordinal_columns = ordinal_columns
        
    def encode(self, df):
        for column, mapping in self.ordinal_columns.items():
            df[column] = df[column].map(mapping)
            logging.INFO(f"Encoded ordinal feature {column} with {len(mapping)} categories")
        return df

