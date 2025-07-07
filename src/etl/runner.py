from etl.factory import create_etl_pipeline
from etl.utils import load_yaml


class Runner:
    def __init__(
        self,
        etl_path: str,
        etl_name: str,
    ):
        self.__etl_path = etl_path
        self.__etl_name = etl_name
        self.__yaml_file = load_yaml(self.__etl_path)

    def run_pipeline(self):
        for pipeline_config in self.__yaml_file.get("pipelines", []):
            ### Step 1: Check if the pipeline exists in the YAML file
            if pipeline_config.get("name") == self.__etl_name:
                try:
                    ### Step 2: Create the ETL pipeline using the factory function
                    pipeline = create_etl_pipeline(pipeline_config)
                    ### Step 3: Run the ETL pipeline
                    pipeline.run()
                except Exception as e:
                    raise Exception(
                        f"Pipeline execution failed for '{self.__etl_name}': {str(e)}"
                    ) from e
                return
        raise Exception(
            f"Pipeline '{self.__etl_name}' not found in '{self.__etl_path}'."
        )
