from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

database_url = config("DATABASE_URL")
test_database_url = config("TEST_DATABASE_URL")