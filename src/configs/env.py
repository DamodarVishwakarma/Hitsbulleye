"""file to contain the env specific configs"""
import os
from functools import lru_cache
from pydantic import BaseSettings


class DBConfig:
    """
    db config
    """
    db_name: str
    db_host: str
    db_username: str
    db_password: str


class AppDBConfig(DBConfig):
    """
    App Db config
    """

    db_host: str = os.getenv("DB_HOST", "localhost")
    db_name: str = os.getenv("DB_NAME", "postgres")
    db_username: str = os.getenv("DB_USERNAME", "postgres")
    db_password: str = os.getenv("DB_PASSWORD", "postgres")


class ESConfig:
    """ES config"""
    es_host: str
    es_port: str


class SearchESConfig:
    """es config"""
    es_host: str = os.getenv("ES_HOST", "localhost")
    es_port: str = os.getenv("ES_PORT", "9200")


class BaseConfig(BaseSettings):
    """Base config"""

    env = os.getenv("APP_ENV", "local")
    db_app: DBConfig = AppDBConfig
    redis_port = os.getenv("BROKER_PORT", 6379)
    redis_host: str = os.getenv("BROKER_HOST", "localhost")
    redis_db: int = 13
    default_dev_email: str = os.getenv("DEFAULT_DEV_EMAIL", "")
    es_question_idx: str = os.getenv("ES_QUESTION_IDX", "es_question_idx")


class AppConfig(BaseConfig):
    es_instance: ESConfig = SearchESConfig
    db_instance: DBConfig = AppDBConfig


class Config:
    @staticmethod
    def get_settings():
        """
        get env
        """
        env = os.getenv("APP_ENV", "local")
        config_select = {
            "dev": AppConfig,
            "test": AppConfig,
            "stage": AppConfig,
            "prod": AppConfig,
            "local": AppConfig,
        }
        return config_select.get(env)


@lru_cache()
def get_settings():
    """get env"""
    return Config.get_settings()()
