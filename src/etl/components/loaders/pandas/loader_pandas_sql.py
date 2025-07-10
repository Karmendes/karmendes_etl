import pandas as pd
from sqlalchemy import create_engine
from etl.etl import Loader

class LoaderPandasSQL(Loader):
    def __init__(self, params: dict):
        self.params = params

    def load(self, data: pd.DataFrame):
        """
        Load a pandas DataFrame to a SQL database using SQLAlchemy engine.
        :param data: DataFrame to be loaded
        """
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Data must be a pandas DataFrame")

        connection_string = self.params.get('connection_string')
        if not connection_string:
            raise ValueError("Connection string is required in params")

        engine = create_engine(connection_string)
        to_sql_params = {k: v for k, v in self.params.items() if k != 'connection_string'}

        data.to_sql(**to_sql_params, con=engine)  