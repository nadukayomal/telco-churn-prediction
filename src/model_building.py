import os
import logging
import joblib
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from typing import List
from sklearn.ensemble import RandomForestClassifier
logging.basicConfig(level = logging.INFO , format = '%(asctime)s - %(levelname)s - %(message)s')


class BaseModelBuilder(ABC):
    """
    Created template for common every type of model buildings
    include : 
        - model building
        - load model
        - save model

    Args : 
        - model_name
        - kwargs : every parameter has on different models
    """
    def __init__(self, model_name , **kwargs):
        self.model_name = model_name
        self.model = None
        self.model_params = kwargs

    @abstractmethod
    def build_model(self):
        pass

    def save_model(self, file_path):
        if self.model is None:
            raise ValueError("No model to save , Build the model first")
        joblib.dump(self.model, file_path)

    def load_model(self, file_path):
        if not os.path.exists(file_path):
            raise ValueError("No model to load on the path")
        self.model = joblib.load(file_path)


class RandomForestModelBuilder(BaseModelBuilder):
    def __init__(self, **kwargs):
        default_params = {
                            'max_depth': 10,
                            'n_estimators': 100,
                            'min_samples_split': 2,
                            'min_samples_leaf': 1,  
                            'random_state': 42    
                        }
        default_params.update(kwargs)
        super().__init__('RandomForest', **default_params)
    
    def build_model(self):
        self.model = RandomForestClassifier(**self.model_params)
        logging.info(f"Building {self.model_name} model")
        return self.model

        

        
