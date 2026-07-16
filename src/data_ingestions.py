import pandas as pd
from abc import ABC, abstractmethod

class DataIngestor(ABC):
    @abstractmethod
    def data_ingest(self, file_path):
        pd.DataFrame()


class DataIngestorCSV(DataIngestor):
    def data_ingest(self, file_path):
        return pd.read_csv(file_path)

class DataIngestorExcel(DataIngestor):
    def data_ingest(self, file_path):
        return pd.read_excel(file_path)