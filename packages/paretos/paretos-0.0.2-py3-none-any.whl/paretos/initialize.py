from .config import config
from .objects.authenticate import CustomerToken


def initialize(
    customer_token: str,
    db_path: str,
    endpoint_url="https://api.paretos.io/socrates/",
):
    customer_token = CustomerToken(customer_token)
    config.initialize(customer_token, db_path, endpoint_url)
