from starlette.config import Config

config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=True)
ONNX_MODEL_NAME = config("ONNX_MODEL_NAME")
LABELS_MAP_PATH = config("LABELS_MAP_PATH")
