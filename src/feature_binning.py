import os
import logging
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class BinningStrategy(ABC):
    @abstractmethod
    def bin_feature(self, column : str, df: pd.DataFrame):
        pass


class CustomBinningStrategy(BinningStrategy):
    def __init__(self, binning_definition):
        self.binning_definition = binning_definition

    def bin_feature(self, column, df):
        # may double check the function
        def assign_bin(value):
            for bin_label, bin_range in self.binning_definition.items():
                if bin_range[0 ]<= value < bin_range[1]:
                    return bin_label
            return "invalied"

        df[f"{column}Bins"] = df[column].apply(assign_bin)
        del df[column]
        logging.info(f"Applied custom bin for {column} and create new column {column}Bins")
        return df

class BinaryBinnig(BinningStrategy):
    def __init__(self, binning_definition):
        self.binning_definition = binning_definition

    def bin_feature(self, column: str, df: pd.DataFrame):
        def assign_bin(value):
            for label , values in self.binning_definition.items():
                if value in values:
                    return label

        df[f"{column}"] = df[column].apply(assign_bin)
        logging.info(f"Applied binary binning for {column}")
        return df
        