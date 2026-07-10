"""
Data pipeline module

This has contain all end to end data processing pipeline
Stages:
    1. Data ingestion
    2. Missing value handling
    3. Outlier detection
    4. Feature binning
    5. Feature encoding
    6. Feature scaling
    7. Post-processing
    8. Train-test splitting
    9. Artifact persistence

"""

from ntpath import exists
import os
import sys
import logging
import json
from matplotlib.cm import binary
import pandas as pd
import numpy as np
from typing import Dict, Optional
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "utils"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from data_ingestions import DataIngestorCSV
from missing_value_handle import DropMissingValueStrategy
from clean_garbage_value import DropColumns, DataTypeConvertor
from feature_binning import CustomBinningStrategy, BinaryBinnig
from feature_encoding import NominalEncodingStrategy, OrdialEncodingStrategy
from feature_scaling import StandardScaleration
from data_splitter import SimpleTrainTestSplitStrategy
from imbalanced_handle import SmoteImbalanceHander
from config import get_path, get_preprocessing, get_logging, get_columns, get_reproducibility



def build_data_pipeline (
                        data_path : str = "data/raw/Telco-Customer-Churn.csv", 
                        target_column : str = "Churn", 
                        test_size : float = 0.2, 
                        force_rebuild : bool = False
                        ):

    # Loading config
    data_path_config = get_path()
    data_preprocess_config = get_preprocessing()
    columns_config = get_columns()
    reproducibility_config = get_reproducibility()

    """Data Ingestions part"""

    print("\n1. Data ingestions process started ..........")
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    raw_data_path = data_path_config.get("data", {}).get("raw", {}) or data_path

    if isinstance(raw_data_path, str) and not os.path.isabs(raw_data_path):
        raw_data_path = os.path.join(root_dir, raw_data_path)
    
    #  Set the path where processed data & artifacts exist 
    processed_data_dir = os.path.join(
                                    os.path.dirname(__file__),
                                    "..",
                                    data_path_config.get("data", {}).get("processed_dir")
                                    )
    artifact_dir = os.path.join(
                                os.path.dirname(__file__), 
                                "..", 
                                data_path_config.get("artifacts", {}).get("root", {})
                                )


    X_train_path = os.path.join(artifact_dir, "X_train.csv")
    X_test_path = os.path.join(artifact_dir, "X_test.csv")
    Y_train_path = os.path.join(artifact_dir, "Y_train.csv")
    Y_test_path = os.path.join(artifact_dir, "Y_test.csv")

    # Check all path are already avilable and is it ok read splited train, test
    all_paths_exist = os.path.exists(X_train_path) and \
                        os.path.exists(X_test_path) and \
                        os.path.exists(Y_train_path) and \
                        os.path.exists(Y_test_path)

    if all_paths_exist:
        X_train = pd.read_csv(X_train_path)
        X_test = pd.read_csv(X_test_path)
        Y_train = pd.read_csv(Y_train_path)
        Y_test = pd.read_csv(Y_test_path)
    
    os.makedirs(artifact_dir, exist_ok=True)


    ingestor = DataIngestorCSV()
    df = ingestor.data_ingest(raw_data_path)
    print(f"Data loaded Shape : {df.shape}")
    # print(df.head(3))

    """ Handle data type conversion and unnecessary column removal """

    print("\n2. Column removal & cast process started ..........") 
    removable_columns = data_preprocess_config.get("drop_columns", {}).get("columns", {})
    column_remover = DropColumns(columns = removable_columns, df = df)
    df = column_remover.drop()

    # Cast column's data type
    columns_to_cast = data_preprocess_config.get("dtype_casting", {})
    column_casting = DataTypeConvertor(columns = columns_to_cast)
    df =  column_casting.casting(df = df)

    """ Handling missing value """

    print("\n3. Misiing value handle process started ..........")
    drop_columns = data_preprocess_config.get("missing_values", {}).get("columns", {})
    drop_missing_value = DropMissingValueStrategy(drop_columns = drop_columns)
    df = drop_missing_value.handle_missing_value(df)
    # print("\n",df.head(3))

    """ Handle feature binnings """

    print("\n4. Feature binning process started ..........")
    custom_binning_definition = (
                                data_preprocess_config
                                .get("feature_binning", {})
                                .get("custom", {})
                                .get("tenure", {})
                                )
    custom_binning = CustomBinningStrategy(binning_definition = custom_binning_definition)
    df = custom_binning.bin_feature(column = "tenure", df = df)
    # print(f"\n{df.head(3)}")

    binary_binning_definition = (
                                data_preprocess_config
                                .get("feature_binning", {})
                                .get("binary", {})
                                .get("Churn", {})
                                )
    binary_binning = BinaryBinnig(binning_definition = binary_binning_definition)
    df = binary_binning.bin_feature(column = "Churn", df = df)
    # print(f"\n{df.head(3)}")

    """ Handle feature encodeing """

    print("\n5. Feature encoding process started ..........")
    nominal_columns = (data_preprocess_config.get("encoding", {}).get("nominal_features", {}))
    nominal_encoding = NominalEncodingStrategy(nominal_columns = nominal_columns)
    df = nominal_encoding.encode(df = df)
    # print(f"\n{df.head(3)}")

    ordinal_column = (data_preprocess_config.get("encoding", {}).get("ordinal_features", {}))
    ordinal_encoding = OrdialEncodingStrategy(ordinal_columns = ordinal_column)
    df = ordinal_encoding.encode(df = df)
    # print(f"\n{df.head(3)}")

    """ Handle feature scaling """

    print("\n6. Feature scaling process started ..........")
    scaling_features = (data_preprocess_config.get("scaling", {}).get("features", {}))
    standing_scaling = StandardScaleration()
    df = standing_scaling.scale(df = df , columns = scaling_features)
    # print(f"\n{df.head(3)}")
    
    """ Data splitting """

    print("\n7. Data splitting process started ..........")
    test_size = (data_preprocess_config.get("split", {}).get("test_size", {}))
    splitting_data = SimpleTrainTestSplitStrategy(test_size = test_size)
    X_train, X_test, Y_train, Y_test = splitting_data.split_data(df = df , target_column = "Churn")

    """ Handle Imbalance """

    print("\n8. Imbalance handle process started ..........")
    random_state = reproducibility_config.get("random_state", {})
    handling_imbalance = SmoteImbalanceHander(random_state = random_state)
    X_train_resample, Y_train_resample = handling_imbalance.handle(X_train, Y_train)

    """ Save data on apath """
    # Save splitted data
    X_train_resample.to_csv(X_train_path, index = False)
    X_test.to_csv(X_test_path, index = False)
    Y_train_resample.to_csv(Y_train_path, index = False)
    Y_test.to_csv(Y_test_path, index = False)
    print("\n9. Data saved on path ..........\n")
   
if __name__ == "__main__":
    build_data_pipeline()
