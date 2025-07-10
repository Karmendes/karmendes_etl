import json
from etl.etl import Loader

class LoaderJson(Loader):
    def __init__(self, path:str):
        self.path = path

    def load(self,data):
        with open(self.path, 'w', encoding='utf-8') as file:
            json.dump(data,file)
            print(f"Data loaded to JSON file at {self.path}")