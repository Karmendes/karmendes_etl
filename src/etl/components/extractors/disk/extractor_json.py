import json
from etl.etl import Extractor


class ExtractorJson(Extractor):
    def __init__(self, paths: list):
        self.paths = paths
        self.list_jsons = []

    def extract(self):
        for path in self.paths:
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    data = file.read()
                    self.list_jsons.append(data)
                
            except FileNotFoundError:
                raise FileNotFoundError(f"Files not found: {path}")
            except json.JSONDecodeError as e:
                raise ValueError(f"Error decoding JSON from files'{path}': {str(e)}") from e
            except Exception as e:
                raise Exception(f"An error occurred while extracting JSON from files'{path}': {str(e)}") from e
        return self.list_jsons