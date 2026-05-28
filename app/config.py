from os import getenv

from dotenv import load_dotenv


load_dotenv()


class BaseConfig:
    ENV_NAME = getenv("FLASK_ENV", "development")
    SECRET_KEY = getenv("SECRET_KEY", "dev-secret")
    API_KEY = getenv("API_KEY", "dev-api-key")
    BASE_URL = getenv("BASE_URL", "http://127.0.0.1:5000")
    MONGO_URI = getenv("MONGO_URI", "mongodb://localhost:27017/ragnarok")
    JSON_SORT_KEYS = False


class DevelopmentConfig(BaseConfig):
    ENV_NAME = "development"
    DEBUG = getenv("FLASK_DEBUG", "true").lower() == "true"


class TestingConfig(BaseConfig):
    ENV_NAME = "testing"
    TESTING = True
    MONGO_URI = getenv("MONGO_TEST_URI", "mongodb://localhost:27017/ragnarok_test")


class ProductionConfig(BaseConfig):
    ENV_NAME = "production"
    DEBUG = False


def get_config(config_name: str | None = None) -> type[BaseConfig]:
    configs = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }

    env_name = config_name or getenv("FLASK_ENV", "development")
    return configs.get(env_name, DevelopmentConfig)
