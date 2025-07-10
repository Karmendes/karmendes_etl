from src.etl.etl import Extractor
from src.etl.handlers.api.requester import HttpClient


class ExtractorGetHttp(Extractor):
    def __init__(self, **kwargs):
        self.config = kwargs
        self.client = HttpClient(
            headers=self.config.get('headers'),
            retries=self.config.get('retries', 2),
            status_to_retry=self.config.get('status_to_retry', (429, 504, 503, 500)),
            backoff_factor=self.config.get('backoff_factor', 2)
        )

    def extract(self):
        return self.client.get(self.config.get('url'), params=self.config.get('params', {}))

class ExtractorPostHttp(Extractor):
    def __init__(self, **kwargs):
        self.config = kwargs
        self.client = HttpClient(
            headers=self.config.get('headers'),
            retries=self.config.get('retries', 2),
            status_to_retry=self.config.get('status_to_retry', (429, 504, 503, 500)),
            backoff_factor=self.config.get('backoff_factor', 2)
        )

    def extract(self):
        # Implement the logic to extract data from Spotify API
        return self.client.post(self.config.get('url'), params=self.config.get('params', {}))