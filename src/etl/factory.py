
from etl.etl import ETL
from etl.components.extractors.databases.extractor_postgres import ExtractorPostgres
from etl.components.loaders.aws.s3 import LoaderS3
from etl.logger import Logger

COMPONENTS_REGISTRY = {
    "extractor_postgres": ExtractorPostgres,
    "loader_s3": LoaderS3,
}


def create_etl_pipeline(config):
    # Extractor
    
    extractor_config = config["extractor"].get("config", {})
    extractor_class = COMPONENTS_REGISTRY[config["extractor"]["type"]]
    extractor = extractor_class(**extractor_config)
    Logger.emit(
        f"Created extractor of type '{config['extractor']['type']}' with config: {extractor_config}",
        log_type=Logger.INFO,
    )


    # Loader
    loader_config = config["loader"].get("config", {})
    loader_class = COMPONENTS_REGISTRY[config["loader"]["type"]]
    loader = loader_class(**loader_config)
    Logger.emit(
        f"Created extractor of type '{config['extractor']['type']}' with config: {extractor_config}",
        log_type=Logger.INFO,
    )

    # Transformer
    transformer_config = config["transformer"]
    transformer_class = COMPONENTS_REGISTRY[transformer_config["type"]]
    transformer = transformer_class(config=transformer_config.get("config", {}))

    return ETL(extractor, loader, transformer)
