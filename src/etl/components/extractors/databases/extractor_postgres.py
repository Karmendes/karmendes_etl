from etl.etl import Extractor


class ExtractorPostgres(Extractor):
    def __init__(self, **kwargs):
        self.config = kwargs

    def extract(self):
        # Implement the logic to extract data from PostgreSQL
        pass