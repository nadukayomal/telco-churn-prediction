import os
import logging
import joblib
import pandas as pd
import numpy as np

logging.basicConfig(
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s'
                    )


class ModelTrainer:
    def train(self, model, X_train, Y_train):
        model.fit(X_train, Y_train)
        train_score = model.score(X_train, Y_train)
        return model, train_score

    def save_model(self, model, file_path):
        joblib.dump(model, file_path)
        logging.info(f"Save model {file_path} file path")

    def load_model(self, file_path):
        return joblib.load(file_path)
