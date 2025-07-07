from etl.etl import Transformer

class PythonTransformer(Transformer):
    def __init__(self, config):
        self.code = config.get("code", "")
        self.compiled_code = None
        self.transform_func = None

        self._compile_and_load()

    def _compile_and_load(self):
        exec_globals = {}
        exec(self.code, exec_globals)

        # Procura pela função transform
        if "transform" not in exec_globals:
            raise ValueError(
                "the code from transformer should set a function 'transform(data)'."
            )

        self.transform_func = exec_globals["transform"]

    def transform(self, data):
        if not self.transform_func:
            raise RuntimeError("Any fucnton 'transform' has been found.")
        return self.transform_func(data)