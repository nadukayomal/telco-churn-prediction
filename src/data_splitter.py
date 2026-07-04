import os
import logging
import pandas as pd
import numpy as np

from abc import ABC, abstractmethod
from sklearn.model_selection import train_test_split
logging.basicConfig(level = logging.INFO, format = "%(asctime)s - %(levelname)s - %(message)s")


class DataSplittingStrategy(ABC):
    @abstractmethod
    def split_data(self, df, target_column):
        pass


class SimpleTrainTestSplitStrategy(DataSplittingStrategy):
    def __init__(self, test_size = 0.2):
        self.test_size = test_size

    def split_data(self, df, target_column):
        Y = df[target_column]
        X = df.drop(columns = [target_column])

        X_train, X_test, Y_train, Y_test = train_test_split(
                                                            X, 
                                                            Y, 
                                                            test_size = self.test_size
                                                            )
        return X_train, X_test, Y_train, Y_test