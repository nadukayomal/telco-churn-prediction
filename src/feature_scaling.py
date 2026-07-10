import os
import logging
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from enum import Enum
from abc import ABC, abstractmethod
from typing import List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
import warnings


class ScalingStrategy(ABC):
    @abstractmethod
    def scale(self, df, columns):
        pass

class ScalingType(str, Enum):
    MINMAX = 'minmax'
    STANDARD = 'standard'

class StandardScaleration(ScalingStrategy):
    def __init__(self):
        self.scaler = StandardScaler()
        self.fitted = False

    def scale(self, df : pd.DataFrame, columns : List):
        df[columns] = self.scaler.fit_transform(df[columns])
        self.fitted = True
        logging.info(f"Applied Standard Scaling for {columns} features")
        return df

    def get_scaler(self):
        return self.scaler
