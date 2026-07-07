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

import os
import sys
import logging
import json
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
from feature_scaling import StandardScaler
from data_splitter import SimpleTrainTestSplitStrategy
from imbalanced_handle import SmoteImbalanceHander
from config import get_path, get_preprocessing, get_logging, get_columns



def build_data_pipeline (
                        data_path : str = "data/raw/Telco-Customer-Churn.csv", 
                        target_column : str = "Churn", 
                        test_size : float = 0.2, 
                        force_rebuild : bool = False
                        ):

    data_path_config = get_path()
    data_preprocess_config = get_preprocessing()
    columns_config = get_columns()

    """Data Ingestions part"""

    print("Data ingestions process")
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    raw_data_path = data_path_config.get("data", {}).get("raw", {}) or data_path

    if isinstance(raw_data_path, str) and not os.path.isabs(raw_data_path):
        raw_data_path = os.path.join(root_dir, raw_data_path)
    
    #  Set the path where processed data exist 
    processed_data_dir = os.path.join(
                                        os.path.dirname(__file__),
                                        "..",
                                        data_path_config.get("data", {}).get("processed_dir")
                                    )






    """ Bellow are remove later only for validate """
    # print("Every compoent has on preprocesing path")
    # for key, val in data_preprocess_config.items():
    #     print(key)
    # print("\nEvery compoent has on data path")
    # for key, val in data_path_config.items():
    #     print(key)
    # print("\nEvery compoent has on columns")
    # for key, val in columns_config.items():
    #     print(key)
    # print(raw_data_path)

build_data_pipeline()
