from requests import Session
from retry_requests import retry
from etl.logger import Logger

class HttpClient:
    def __init__(self, headers=None, session=None, retries=2, status_to_retry=(429,408,504,503,500), backoff_factor=2):
        self.session = session or retry(Session(), retries=retries, backoff_factor=backoff_factor, status_to_retry=status_to_retry)
        if headers:
            self.session.headers.update(**headers)
        self.session.hooks = {
            'response': lambda r, *args, **kwargs: self._raise_trace(r)
        }

    def _raise_trace(self, resp):
        Logger.emit(f"HTTP response: {resp.status_code} - {resp.url}")
        resp.raise_for_status()

    def get(self, url, **params):
        Logger.emit(f'HTTP GET: {url} Params: {params}')
        return self.session.get(url, **params)

    def post(self, url, **params):
        Logger.emit(f'HTTP POST: {url} Params: {params}')
        return self.session.post(url, **params)