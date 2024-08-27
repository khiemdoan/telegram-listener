__author__ = 'Khiem Doan'
__github__ = 'https://github.com/khiemdoan'
__email__ = 'doankhiem.crazy@gmail.com'
__url__ = 'https://github.com/khiemdoan/clean-architecture-python-boilerplate/blob/main/src/settings/opensearch.py'

from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenSearchSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: str

    model_config = SettingsConfigDict(
        extra='ignore',
        env_prefix='OPENSEARCH_',
        env_file='.env',
        env_file_encoding='utf-8',
    )
