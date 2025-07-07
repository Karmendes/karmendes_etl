# ETL Pipeline Package Documentation

## Overview

This package is designed to simplify the creation and management of ETL (Extract, Transform, Load) pipelines. It allows you to configure and run ETL workflows based on a YAML configuration file, making it highly flexible and extensible for various data processing tasks.

The ETL pipeline consists of three main components: **Extractor**, **Transformer**, and **Loader**. These components can be easily configured and extended by users to meet specific use cases. The package also supports parallel execution, error handling, and logging, offering a streamlined approach to managing data workflows.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Key Components](#key-components)
3. [Usage](#usage)
4. [Configuration](#configuration)
5. [Extending the Package](#extending-the-package)
6. [Testing and CI/CD](#testing-and-cicd)
7. [Roadmap for Improvements](#roadmap-for-improvements)

---

## Architecture Overview

The core of the ETL package is structured around the **Extractor**, **Transformer**, and **Loader** components:

- **Extractor**: Responsible for fetching data from an external source.
- **Transformer**: Takes the extracted data and applies necessary transformations.
- **Loader**: Loads the transformed data into the target destination.

### ETL Flow
The ETL pipeline flow is as follows:
1. **Extract**: Data is fetched using the `Extractor`.
2. **Transform**: The data is processed and transformed using the `Transformer`.
3. **Load**: The transformed data is then loaded into the destination using the `Loader`.

### Factory Pattern

The `factory.py` file contains a factory function that dynamically creates the ETL pipeline based on the YAML configuration file. This allows flexibility in defining custom pipelines that integrate different extractors, transformers, and loaders.

---

## Key Components

### 1. **Extractor**

The **Extractor** class is the base class for all extractors. It defines an abstract method `extract()` that must be implemented by any subclass. Common extractors might include database extractors, file extractors, or API-based extractors.

#### Example:
```python
class Extractor(ABC):
    @abstractmethod
    def extract(self):
        pass
```

### 2. **Transformer**

The **Transformer** class is the base class for transformation logic. It defines an abstract method `transform(data)` that must be implemented by any subclass. Transformations might involve data cleaning, enrichment, or aggregation.

#### Example:
```python
class Transformer(ABC):
    @abstractmethod
    def transform(self, data):
        pass
```

### 3. **Loader**

The **Loader** class is the base class for all loaders. It defines an abstract method `load(data)` that must be implemented by any subclass. Loaders are responsible for writing the transformed data into a target location, such as a database, file system, or data warehouse.

#### Example:
```python
class Loader(ABC):
    @abstractmethod
    def load(self, data):
        pass
```

### 4. **ETL Pipeline**

The **ETL** class orchestrates the ETL process. It takes an extractor, loader, and transformer as inputs and coordinates their execution.

#### Example:
```python
class ETL:
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
```

### 5. **Factory**

The `factory.py` file contains a mapping of component names to their respective classes and a `create_etl_pipeline` function to dynamically create the ETL pipeline based on the YAML configuration.

#### Example:
```python
COMPONENTS_REGISTRY = {
    "extractor_postgres": ExtractorPostgres,
    "loader_s3": LoaderS3,
}

def create_etl_pipeline(config):
    extractor_class = COMPONENTS_REGISTRY[config["extractor"]["type"]]
    extractor = extractor_class(**config["extractor"].get("config", {}))

    loader_class = COMPONENTS_REGISTRY[config["loader"]["type"]]
    loader = loader_class(**config["loader"].get("config", {}))

    transformer_class = COMPONENTS_REGISTRY[config["transformer"]["type"]]
    transformer = transformer_class(config=config["transformer"].get("config", {}))

    return ETL(extractor, loader, transformer)
```

---

## Usage

### Running the ETL Pipeline

You can run the pipeline via the command line by specifying the path to the YAML configuration file and the pipeline name.

#### Example Command:
```bash
python runner.py config.yaml etl-gmail-to-landing-accounts
```

This will:
1. Load the configuration from `config.yaml`.
2. Create the ETL pipeline for the pipeline name `etl-gmail-to-landing-accounts`.
3. Execute the pipeline.

---

## Configuration

The configuration for the pipelines is specified in a YAML file. The configuration defines the extractors, transformers, and loaders used in each pipeline, along with their respective parameters.

### Example Configuration:
```yaml
pipelines:
  - name: etl-gmail-to-landing-accounts
    extractor:
      type: ExtractorPostgres
      config:
        user: postgres
        password: postgres
        host: localhost
        port: 5432
        database: gmail
    loader:
      type: LoaderS3
      config:
        bucket: my-landing-bucket
        prefix: landing-data
    transformer:
      type: PythonTransformer
      config:
        code: |
          def transform(data):
            for i, value in enumerate(data):
              data[i]["data"] = decode(value["data"], "tz.gzip")
            return data
```

---

## Extending the Package

### Adding a New Extractor
To add a new extractor, subclass the `Extractor` class and implement the `extract()` method. Then, register the new class in the `COMPONENTS_REGISTRY` dictionary.

### Adding a New Transformer
To add a new transformer, subclass the `Transformer` class and implement the `transform(data)` method. Then, register the new class in the `COMPONENTS_REGISTRY` dictionary.

### Adding a New Loader
To add a new loader, subclass the `Loader` class and implement the `load(data)` method. Then, register the new class in the `COMPONENTS_REGISTRY` dictionary.

---

## Roadmap for Improvements

Here are planned improvements and features to enhance the package’s scalability, reliability, and flexibility:


1. **Implement Data Contracts**
    - Introduce data contracts to enforce data quality expectations across the pipeline.

2. **Notifications and Alerts**
   - Integrate with messaging services like Gchat or email to notify users of pipeline execution status.

3. **Implement Logging and Monitoring**
   - Add detailed logging for various levels (INFO, DEBUG, ERROR).

4. **Validate YAML Configuration**
   - Add configuration validation using libraries like `pydantic` or `Cerberus`.
   - Ensure that all required fields are present and that the data types are correct.

5. **CI/CD and Automated Testing**
   - Add unit and integration tests.
   - Configure CI tools like GitHub Actions to run tests and deploy the pipeline automatically.

---

## Conclusion

This ETL pipeline package offers a flexible and extensible solution for managing and running data pipelines. It is easy to configure, extend, and scale according to your needs. The roadmap highlights planned improvements that will enhance the package's capabilities and ensure it remains robust for production environments.