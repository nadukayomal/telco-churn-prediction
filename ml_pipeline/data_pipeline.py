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
from config import get_path, get_preprocessing, get_logging
