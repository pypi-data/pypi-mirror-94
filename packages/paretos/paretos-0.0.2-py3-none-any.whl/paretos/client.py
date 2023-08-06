from urllib.parse import urljoin

from . import OptimizationProblem
from .authenticator import SocratesAPIAuth
from .exceptions import handle_error_response
from .objects import Designs
from .objects.analyzed_results import AnalyzedEvaluations
from .objects.authenticate import AccessToken, CustomerToken
from .objects.enums import RequestMethods
from .objects.evaluation import Evaluations
from .objects.progress import Progress
from .session import SocratesAPISession


class SocratesAPIClient(object):
    def __init__(self, api_url: str, customer_token: str):
        """
        Instantiate a new API client.
        :param api_url: url of the api
        :param customer_token: string containing the customer credentials
        """
        self.__url = api_url
        self.__session = SocratesAPISession()
        self.__authenticator = SocratesAPIAuth(
            self, CustomerToken(token=customer_token)
        )

    @staticmethod
    def __get_versioned_path(path: str, version: str = "v1") -> str:
        return f"{version}/{path}"

    # Perform an API request.
    def __request(
        self,
        path: str,
        version: str,
        data: dict = None,
        authenticate: bool = False,
        method="POST",
    ):
        if method not in RequestMethods.__members__:
            raise ValueError("Invalid Request method chosen.")

        if authenticate:
            self.__session.auth = self.__authenticator
        else:
            self.__session.auth = None

        path = self.__get_versioned_path(path, version)
        # with the parameters provided.

        # TODO: Talk to Janik what happsn here somehow there is something happening...
        # Somehow here python is calling the first time the wrong request and we
        # Have here weired data atm...
        resp = self.__session.request(method, urljoin(self.__url, path), json=data)

        # If something goes wrong, we'll pass the response
        # off to the error-handling code
        if resp.status_code >= 400:
            handle_error_response(resp)

        response_json = resp.json()
        if response_json["status"] != "success":
            handle_error_response(resp)

        # Otherwise return the result dictionary.
        return response_json["data"]

    # API methods
    def authenticate(
        self, customer_token: CustomerToken, version: str = "v1"
    ) -> AccessToken:
        response = self.__request(
            "authenticate", version, customer_token.to_dict(), authenticate=False
        )

        return AccessToken.from_dict(response)

    def __problem_request(
        self,
        path: str,
        version: str,
        problem: OptimizationProblem,
        evaluations: Evaluations,
        additional_data: dict = None,
    ):
        if additional_data is None:
            additional_data = {}

        problem_data = {
            "problem": problem.as_dict(),
            "evaluations": evaluations.as_list_of_dicts(),
        }

        data = {**problem_data, **additional_data}

        return self.__request(path, version, data, authenticate=True)

    def predict_design(
        self,
        problem: OptimizationProblem,
        evaluations: Evaluations,
        quantity: int,
        version: str = "v1",
    ) -> Designs:
        response = self.__problem_request(
            "design/predict", version, problem, evaluations, {"quantity": quantity}
        )

        return Designs.from_list_of_list(response["designs"])

    def track_progress(
        self,
        problem: OptimizationProblem,
        evaluations: Evaluations,
        version: str = "v1",
    ) -> Progress:
        response = self.__problem_request(
            "progress/track", version, problem, evaluations
        )

        return Progress.from_dict(response)

    def analyze_result(
        self,
        problem: OptimizationProblem,
        evaluations: Evaluations,
        version: str = "v1",
    ) -> AnalyzedEvaluations:
        response = self.__problem_request(
            "result/analyze", version, problem, evaluations
        )

        return AnalyzedEvaluations.from_list_of_dicts(response["evaluations"])
