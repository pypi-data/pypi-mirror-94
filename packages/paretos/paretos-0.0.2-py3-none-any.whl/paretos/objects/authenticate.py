from __future__ import annotations

from datetime import datetime, timedelta, timezone

TOKEN_BUFFER_SECONDS = 60


class AccessToken:
    def __init__(self, access_token: str, expires: datetime):
        self.__token = access_token
        self.__expires = expires

    def get_access_token(self) -> str:
        return self.__token

    def is_token_expired(self) -> bool:
        buffer = timedelta(seconds=TOKEN_BUFFER_SECONDS)
        return datetime.now(tz=timezone.utc) + buffer > self.__expires

    @classmethod
    def from_dict(cls, from_dict: dict) -> AccessToken:
        access_token = from_dict["accessToken"]
        expiration_iso8601 = from_dict["accessTokenExpiration"]
        expiration_date = datetime.fromisoformat(expiration_iso8601)

        return cls(access_token=access_token, expires=expiration_date)


class CustomerToken:
    def __init__(self, token: str):
        self.__token = token

    @property
    def token(self) -> str:
        return self.__token

    def to_dict(self) -> dict:
        return {"customerToken": self.token}
