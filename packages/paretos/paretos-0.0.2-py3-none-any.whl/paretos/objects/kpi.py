from typing import List

from paretos.objects.enums import Goals, ParameterTypes

from .parameter import Parameter, ParameterSpace, ParameterValues


class KpiParameter(Parameter):
    """
    Describes a single KPI Parameter which should be considered as an optimization goal
    """

    def __init__(self, id: str, goal: Goals = Goals.minimize):
        super().__init__(id, ParameterTypes.kpi)

        if not self.is_valid_goal(goal):
            raise ValueError(
                f"It can only be chosen between: ['minimize', 'maximize']. The value "
                f"{goal} ist not permitted"
            )

        self.__goal = goal

    def get_goal(self) -> Goals:
        return self.__goal

    @staticmethod
    def is_valid_goal(goal: Goals) -> bool:
        return isinstance(goal, Goals)

    def as_dict(self) -> dict:
        parameter_dict = super().as_dict()
        parameter_dict["goal"] = self.get_goal().name

        return parameter_dict


class KpiValues(ParameterValues):
    pass


class KpiSpace(ParameterSpace):
    """
    Class describing the set of all design parameters for a specific problem
    """

    def __init__(self, parameters: List[KpiParameter] = None):
        super().__init__(parameters)
