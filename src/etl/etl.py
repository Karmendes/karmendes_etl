from abc import ABC, abstractmethod


class Extractor(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def extract(self):
        pass


class Loader(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def load(self, data):
        pass


class Transformer(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def transform(self, data):
        pass


class ETL(ABC):
    def __init__(self, extractor: Extractor, loader: Loader, transformer: Transformer):
        self.extractor = extractor
        self.loader = loader
        self.transformer = transformer

    def extract(self):
        return self.extractor.extract()

    def transform(self, data):
        return self.transformer.transform(data)

    def load(self, data):
        self.loader.load(data)

    def run(self):
        data = self.extract()
        transformed_data = self.transform(data)
        self.load(transformed_data)
