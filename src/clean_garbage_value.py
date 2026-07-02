"""
Handles data type conversions and removal of unnecessary columns
during the preprocessing stage.
"""
import os
import logging
import pandas as pd
import numpy as np
from ast import Dict, List


class DropColumns:
    """ Drops unnecessary columns from a DataFrame during preprocessing."""
    def __init__(self, columns: List, df: pd.DataFrame):
        self.columns = columns
        self.df = df

    def drop(self):
        cleaned_df = self.df.drop(columns=self.columns)
        logging.INFO(f"Drop {self.columns} feature from the data set")
        return cleaned_df


class DataTypeConvertor:
    """ Cast columns to their expected type """
    def __init__(self, columns: Dict, df: pd.DataFrame):
        self.columns = columns
        self.df = df

    def casting_column(self):
        for col, d_type in self.columns.items():
            if d_type == "object":
                self.df[col] = self.df[col].astype(object)
                logging.INFO(f"Casted the {col} data type into {d_type}")
            if d_type == "int":
                self.df[col] = self.df[col].astype(int)
                logging.INFO(f"Casted the {col} data type into {d_type}")

        return self.df
