import os
import logging
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class MissingValueHandle(ABC):
    @abstractmethod
    def handle_missing_value(self, df):
        pass


class DropMissingValueStrategy(MissingValueHandle):
    def __init__(self, drop_columns):
        self.drop_columns = drop_columns
        logging.INFO(f"Drop raws with containg null values from {self.drop_columns}")

    def handle_missing_value(self, df):
        df_cleaned = df.dropna(subset = self.drop_columns)
        droped_raws = len(df) - len(df_cleaned)
        logging.INFO(f"Droped {droped_raws} number of rows from {self.drop_columns}")
        return df_cleaned