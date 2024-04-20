import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent

# Email settings
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = os.environ.get('SMTP_PORT')
SMTP_USER = os.environ.get('SMTP_USER')


class Settings(BaseSettings):
    # DataBase settings
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    # Test DataBase settings
    DB_HOST_TEST: str
    DB_PORT_TEST: str
    DB_USER_TEST: str
    DB_PASS_TEST: str
    DB_NAME_TEST: str

    # JWT token settings
    jwy_public_key: str = (BASE_DIR / 'certs' / 'jwt-public.pem').read_text()
    jwt_private_key: str = (BASE_DIR / 'certs' / 'jwt-private.pem').read_text()
    jwt_algorithm: str = 'RS256'
    jwt_expiration: int = 3600

    @property
    def db_url(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def db_url_test(self):
        return (f'postgresql+asyncpg://{self.DB_USER_TEST}:{self.DB_PASS_TEST}@'
                f'{self.DB_HOST_TEST}:{self.DB_PORT_TEST}/{self.DB_NAME_TEST}')

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
