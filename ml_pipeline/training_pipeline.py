import os
from pyexpat import model
import sys
import logging
import pandas as pd
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from mlflow_utils import MLflowTracker, setup_mlflow_autolog, create_mlflow_run_tags
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

    """ mlflow define """
    mlflow_tracker = MLflowTracker()
    setup_mlflow_autolog()
    run_tags = create_mlflow_run_tags(
                                    "training_pipeline",{
                                        "model_type" : "Random Forest",
                                        "training-strategy" : "simple"
                                        }
                                    )
    run = mlflow_tracker.start_run(run_name = "training_pipeline", tags = run_tags)
    """ mlflow define end """

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
        evaluation_result_cp = evaluation_result.copy()
        evaluation_result_cp.pop("cm", None)

        # print(evaluation_result)

    # Mlflow tracking part
    mlflow_tracker.log_training_metrics(model, evaluation_result_cp, model_params)
    mlflow_tracker.end_run()

if __name__ == "__main__":
    model_path = get_path().get("model",{})["model_path"]
    model_params = get_path().get("model",{})["model_params"]
    # processed_data_path = get_path().get("artifacts", {}).get("data", {})
    training_pipeline(model_params=model_params)