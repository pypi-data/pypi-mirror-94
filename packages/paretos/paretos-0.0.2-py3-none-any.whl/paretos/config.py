import pathlib

from .exceptions import ConfigError, InitializationError
from .lib import is_valid_url
from .objects.authenticate import CustomerToken


def check_initialized(f):
    def wrapper(*args):
        if not args[0].is_initialized():
            raise InitializationError(
                "config has not been initialized. Make sure to run paretos.initialize."
            )
        return f(*args)

    return wrapper


class Config(object):
    def __init__(self):
        self.__customer_token = None
        self.__db_path = None
        self.__initialized = False
        self.__api_url = None

    def initialize(self, customer_token: CustomerToken, db_path, api_url: str):
        self.__initialized = True
        self.__set_db_path(db_path)
        self.__set_customer_token(customer_token)
        self.__set_api_url(api_url)

    @check_initialized
    def get_customer_token(self) -> CustomerToken:
        return self.__customer_token

    def __set_customer_token(self, customer_token: CustomerToken):
        self.__customer_token = customer_token

    @check_initialized
    def get_db_path(self) -> pathlib.PurePath:
        return self.__db_path

    def __set_db_path(self, db_path):
        if isinstance(db_path, str):
            db_path = pathlib.Path(db_path)

        if not isinstance(db_path, pathlib.PurePath):
            raise ConfigError(f"'{db_path}' is not a valid path")

        self.__db_path = db_path

    def is_initialized(self) -> bool:
        return self.__initialized

    def __set_api_url(self, api_url: str):
        if not is_valid_url(api_url):
            raise ConfigError(f"'{api_url}' is not a valid url")

        if api_url[len(api_url) - 1] != "/":
            api_url = api_url + "/"

        self.__api_url = api_url

    @check_initialized
    def get_api_url(self) -> str:
        return self.__api_url


config = Config()
