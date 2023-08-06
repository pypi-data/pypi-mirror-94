from __future__ import annotations

from typing import List


class AnalyzedEvaluation:
    """
    Class inheriting one evaluation and the information about pareto optimality
    """

    def __init__(self, id: str, is_pareto_optimal: bool):
        self.__id = id
        self.__is_pareto_optimal = is_pareto_optimal

    def get_id(self) -> str:
        return self.__id

    def is_pareto_optimal(self) -> bool:
        return self.__is_pareto_optimal

    @classmethod
    def from_dict(cls, from_dict: dict) -> AnalyzedEvaluation:
        return cls(
            id=from_dict["evaluationId"], is_pareto_optimal=from_dict["isParetoOptimal"]
        )


class AnalyzedEvaluations:
    """
    Class mapping all evaluations with the information from api about pareto optimality
    """

    def __init__(self, analyzed_evaluations: List[AnalyzedEvaluation] = None):
        if analyzed_evaluations is None:
            analyzed_evaluations = []

        self.__analyzed_evaluations = analyzed_evaluations
        self.__evaluations = self.__get_evaluation_ids()
        self.__pareto_evaluations = self.__get_evaluation_ids(True)

    def __get_evaluation_ids(self, only_pareto: bool = False):
        return [
            evaluation.get_id()
            for evaluation in self.__analyzed_evaluations
            if (evaluation.is_pareto_optimal() or not only_pareto)
        ]

    def get_evaluations(self) -> List[str]:
        return self.__evaluations

    def get_pareto_evaluations(self) -> List[str]:
        return self.__pareto_evaluations

    @classmethod
    def from_list_of_dicts(cls, list_of_dicts: List[dict]) -> AnalyzedEvaluations:
        return cls(
            [AnalyzedEvaluation.from_dict(evaluation) for evaluation in list_of_dicts]
        )
