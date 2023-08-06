import logging

# Take a HTTP response object and translate it into an Exception
# instance.
from typing import Dict

from requests import Response


def handle_error_response(resp: Response):
    # Mapping of API response reasons to exception classes
    reasons = {
        -1: SocratesAPIError,
        "02309c4c-adb9-4342-bac8-5058f6d3b41a": InvalidCustomerTokenError,
        "1ac03ba3-1b72-488c-af79-aadda2b9dd4b": ParseError,
        "69147172-c48d-4f25-a014-3885b789b9d1": SchemaValidationError,
    }

    response_json = resp.json()

    if "status" not in response_json:
        error = {"reason": -1, "description": "General API Error", "details": {}}
    else:
        error = response_json["data"]

    logging.info(error)

    description = error.get("description")
    reason = error.get("reason", -1)
    details = error.get("details", {})

    # Build the appropriate exception class with as much
    # details as we can pull from the API response and raise
    # it.
    # reason = reason if reason in reasons else -1
    raise reasons[reason](
        description=description, reason=reason, details=details, response=resp
    )


class ParetosError(Exception):
    pass


class ConfigError(ParetosError):
    pass


class InitializationError(ParetosError):
    pass


class SocratesAPIError(ParetosError):
    response = None
    details = {}
    reason = -1
    description = "An unknown error occurred"

    def __init__(
        self,
        description: str = None,
        reason: str = None,
        details: Dict = None,
        response: Response = None,
    ):
        self.response = response
        if description:
            self.description = description
        if reason:
            self.reason = reason
        if details:
            self.details = details

    def __str__(self):
        if self.reason:
            return "{}: {}".format(self.reason, self.description)
        return self.description


# Specific exception classes


class ParseError(SocratesAPIError):
    pass


class SchemaValidationError(SocratesAPIError):
    pass


class InvalidCustomerTokenError(SocratesAPIError):
    pass
