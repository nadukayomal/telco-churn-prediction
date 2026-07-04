import os
import logging
from imblearn.over_sampling import SMOTE
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



class ImbalanceStrategy(ABC):
    abstractmethod
    def handle(self, X_train, Y_train):
        self.X_train = X_train
        self.Y_train = Y_train
        pass


class SmoteImbalanceHander(ImbalanceStrategy):
    def __init__(self, random_state = 42):
        self.random_state = random_state

    def handle(self, X_train, Y_train):
        smote = SMOTE(random_state= self.random_state)
        X_train_resample, Y_train_resample = smote.fit_resample(self.X_train, self.Y_train)
        logging.INFO(
            f"Handled imbalance ration using SMOTE X_train:{self.X_train.shape} -> {self.X_train_resample.shape} and Y_train : {self.Y_train.shape} -> {self.Y_train_resample.shape}"
        )
        return X_train_resample, Y_train_resample
