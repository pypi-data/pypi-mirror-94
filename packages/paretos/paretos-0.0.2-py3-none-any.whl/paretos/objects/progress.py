from __future__ import annotations


class Progress:
    """
    Mapping to API object for progress
    """

    def __init__(self, nr_of_evaluations: int, nr_of_pareto_points: int):
        self.__nr_of_evaluations = nr_of_evaluations
        self.__nr_of_pareto_points = nr_of_pareto_points

    def get_nr_of_evaluations(self) -> int:
        return self.__nr_of_evaluations

    def get_nr_of_pareto_points(self) -> int:
        return self.__nr_of_pareto_points

    @classmethod
    def from_dict(cls, from_dict: dict) -> Progress:
        return cls(
            nr_of_evaluations=from_dict["nrOfEvaluations"],
            nr_of_pareto_points=from_dict["nrOfParetoPoints"],
        )
