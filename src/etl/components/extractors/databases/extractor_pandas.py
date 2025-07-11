import pandas as pd
from sqlalchemy import create_engine
from etl.etl import Extractor


class ExtractorPandasSQL(Extractor):
    def __init__(self, params):
        self.config = params

    def extract(self):
        """
        Extract data from PostgreSQL using SQLAlchemy engine.
        :return: DataFrame containing the extracted data
        """
        connection_string = self.config.get('connection_string')
        if not connection_string:
            raise ValueError("Connection string is required in params")
        
        engine = create_engine(connection_string)
        query = self.config.get('query')
        if not query:
            raise ValueError("Query is required in config")
        
        return pd.read_sql(query, con=engine)