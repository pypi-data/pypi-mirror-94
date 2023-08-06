import requests

from .version import VERSION


class SocratesAPISession(requests.Session):
    """
    session for consistent requests within the bundle
    """

    def __init__(self):
        super(SocratesAPISession, self).__init__()

        self.headers.update(
            {
                "Accept-Charset": "utf-8",
                "Content-Type": "application/json",
                "User-Agent": "paretos-greek/{}".format(VERSION),
            }
        )
