"""
Handles data type conversions and removal of unnecessary columns
during the preprocessing stage.
"""
import os
import logging
import pandas as pd
import numpy as np
from ast import Dict, List
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class DropColumns:
    """ Drops unnecessary columns from a DataFrame during preprocessing."""
    def __init__(self, columns: List, df: pd.DataFrame):
        self.columns = columns
        self.df = df

    def drop(self):
        cleaned_df = self.df.drop(columns=self.columns)
        logging.info(f"Drop {self.columns} feature from the data set")
        return cleaned_df


class DataTypeConvertor:
    """ Cast columns to their expected type """
    def __init__(self, columns: Dict):
        self.columns = columns

    def casting(self, df):
        for data in self.columns:
            col = data["column"].strip()
            from_type = data["from"].strip()
            to_type = data["to"].strip()

            if to_type == "object":
                df[col] = df[col].astype(object)
                logging.info(f"Casted the {col} data type into {to_type}")
            if to_type == "int":
                df[col] = pd.to_numeric(df[col], errors="coerce")
                logging.info(f"Casted the {col} data type into {to_type}")
            if to_type == "float":
                df[col] = pd.to_numeric(df[col], errors="coerce")
                logging.info(f"Casted the {col} data type into {to_type}")

        return df
