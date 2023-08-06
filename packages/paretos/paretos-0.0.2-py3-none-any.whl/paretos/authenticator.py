from requests.auth import AuthBase

from paretos.objects.authenticate import CustomerToken

TOKEN_BUFFER_SECONDS = 60


class SocratesAPIAuth(AuthBase):
    def __init__(self, client, customer_token: CustomerToken):
        self.__customer_token = customer_token
        self.__client = client
        self.__access_token = None

    def __is_access_token_expired(self) -> bool:
        if self.__access_token is None:
            return True
        return self.__access_token.is_token_expired()

    def __update_access_token(self):
        self.__access_token = self.__client.authenticate(self.__customer_token)

    def __call__(self, r):
        if self.__is_access_token_expired():
            self.__update_access_token()

        r.headers["Authorization"] = "Bearer {}".format(
            self.__access_token.get_access_token()
        )

        return r
