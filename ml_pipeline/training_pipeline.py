import os
from pyexpat import model
import sys
import logging
import pandas as pd
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from model_training import ModelTrainer
from model_building import RandomForestModelBuilder 
from model_evalution import ModelEvaluators
from data_pipeline import build_data_pipeline
from config import (
                    get_path, 
                    get_training, 
                    get_evaluation, 
                    get_reproducibility
                    )
logging.basicConfig(
                    level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    )
logger = logging.getLogger(__name__) 



def training_pipeline(
                        data_path = "data/raw/Telco-Customer-Churn.csv", 
                        model_params = None, 
                        test_size = 0.2, 
                        random_state = 42, 
                        model_path = "model/telco_churn_analysis.joblib"
                    ):

    model_path = get_path().get("model",{})["model_path"]
    model_params = get_path().get("model",{})["model_params"]
    processed_data_path = get_path().get("artifacts", {}).get("data", {})

    # If not exist processed data then re-run data pipeline to generate data set
    if not os.path.exists(processed_data_path["X_train"]) or\
        not os.path.exists(processed_data_path["X_train"]) or\
        not os.path.exists(processed_data_path["X_train"]) or\
        not os.path.exists(processed_data_path["X_train"]):

        build_data_pipeline()

    else:
        print("Loading artifacts from Data pipeline")

        # Get processed data 
        X_train = pd.read_csv(processed_data_path["X_train"])
        X_test = pd.read_csv(processed_data_path["X_test"])
        Y_train = pd.read_csv(processed_data_path["Y_train"])
        Y_test = pd.read_csv(processed_data_path["Y_test"])

        # Build model
        model_builder = RandomForestModelBuilder(**model_params)
        model = model_builder.build_model()

        # Model training
        trainer = ModelTrainer()
        model, train_score = trainer.train(model, X_train, Y_train)

        # Save model
        trainer.save_model(model, model_path)
        # Evaluate model
        evaluator = ModelEvaluators(model, "RandomForest")
        evaluation_result = evaluator.evaluate(X_test, Y_test)
        # evaluation_result_cp = evaluation_result.copy()

        print(evaluation_result)

if __name__ == "__main__":
    model_path = get_path().get("model",{})["model_path"]
    model_params = get_path().get("model",{})["model_params"]
    # processed_data_path = get_path().get("artifacts", {}).get("data", {})
    training_pipeline(model_params=model_params)

