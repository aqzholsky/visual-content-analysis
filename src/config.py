from starlette.config import Config

config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=True)
ONNX_MODEL_NAME = config("ONNX_MODEL_NAME")
LABELS_MAP_PATH = config("LABELS_MAP_PATH")
MONGODB_URL = config("MONGODB_URL")
MAX_CONNECTIONS_COUNT = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT = config("MIN_CONNECTIONS_COUNT", cast=int, default=1)
