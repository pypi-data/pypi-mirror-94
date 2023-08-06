from __future__ import annotations

from typing import Iterator, List

from .enums import ParameterTypes
from .parameter import Parameter, ParameterSpace, ParameterValues


class DesignParameter(Parameter):
    """
    Class describing a single design parameter including its options
    """

    def __init__(self, id: str, minimum: float, maximum: float):
        super().__init__(id, ParameterTypes.design)
        self.__minimum = minimum
        self.__maximum = maximum

    def get_minimum(self) -> float:
        return self.__minimum

    def get_maximum(self) -> float:
        return self.__maximum

    def as_dict(self) -> dict:
        parameter_dict = super().as_dict()
        parameter_dict["minimum"] = self.get_minimum()
        parameter_dict["maximum"] = self.get_maximum()

        return parameter_dict


class DesignValues(ParameterValues):
    pass


class DesignSpace(ParameterSpace):
    def __init__(self, parameters: List[DesignParameter] = None):
        super().__init__(parameters)


class Designs:
    """
    Class containing a lot of designs to be simulated
    """

    def __init__(self, designs: List[DesignValues] = None):
        if designs is None:
            designs = []

        self.__designs = designs

    def __iter__(self) -> Iterator[DesignValues]:
        return iter(self.get_designs())

    def get_designs(self) -> List[DesignValues]:
        return self.__designs

    @classmethod
    def from_list_of_list(cls, list_of_list: List[list]) -> Designs:
        return cls(
            [
                DesignValues.from_list_of_dicts(design_list)
                for design_list in list_of_list
            ]
        )
