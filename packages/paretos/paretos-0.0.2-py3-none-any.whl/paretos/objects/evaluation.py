from typing import List

from paretos.objects import DesignValues, KpiValues


class Evaluation:
    """
    Class for a single evaluation with matching design and kpis
    """

    def __init__(self, id: str, design: DesignValues, kpis: KpiValues):
        self.__id = id
        self.__design = design
        self.__kpis = kpis

    def get_id(self) -> str:
        return self.__id

    def get_design(self) -> DesignValues:
        return self.__design

    def get_kpis(self) -> KpiValues:
        return self.__kpis

    def as_dict(self) -> dict:
        design = self.get_design().as_list_of_dicts()
        kpis = self.get_kpis().as_list_of_dicts()
        return {"id": self.get_id(), "design": design, "kpis": kpis}


class Evaluations:
    """
    Class containing all evaluations
    """

    def __init__(self, evaluation: List[Evaluation] = None):
        if evaluation is None:
            evaluation = []
        self.__evaluations = evaluation

    def get_evaluations(self) -> List[Evaluation]:
        return self.__evaluations

    def add_evaluation(self, evaluation: Evaluation):
        self.__evaluations.append(evaluation)

    def as_list_of_dicts(self) -> List[dict]:
        return [evaluation.as_dict() for evaluation in self.get_evaluations()]
