from pathlib import Path

from dotenv import load_dotenv
import os

load_dotenv()
BASE_DIR = Path(__file__).parent

# Database settings
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_NAME = os.environ.get('DB_NAME')
DB_TEST_NAME = os.environ.get('DB_TEST_NAME')

# JWT token settings
jwy_public_key: str = (BASE_DIR / 'certs' / 'jwt-public.pem').read_text()
jwt_private_key: str = (BASE_DIR / 'certs' / 'jwt-private.pem').read_text()
jwt_algorithm: str = 'RS256'
jwt_expiration: int = 3600

# Email settings
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = os.environ.get('SMTP_PORT')
SMTP_USER = os.environ.get('SMTP_USER')
