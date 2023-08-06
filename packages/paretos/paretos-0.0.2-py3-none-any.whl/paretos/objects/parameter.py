from __future__ import annotations

from typing import Iterator, List, TypeVar

from paretos.objects.enums import ParameterTypes

ParameterT = TypeVar("ParameterT", bound="Parameter")


class Parameter:
    """
    Parent class for all parameter classes‚
    """

    def __init__(self, id: str, type: ParameterTypes):
        if not isinstance(type, ParameterTypes):
            raise ValueError("Invalid Parameter Type")

        self.__id = id
        self.__type = type

    def get_id(self) -> str:
        return self.__id

    def get_type(self) -> ParameterTypes:
        return self.__type

    def as_dict(self) -> dict:
        return {"id": self.get_id()}


class ParameterSpace:
    """
    Class describing the set of all design parameters for a specific problem
    """

    def __init__(self, parameters: List[ParameterT]):
        self.__parameters = parameters

    def __iter__(self) -> Iterator[ParameterT]:
        return iter(self.__parameters)

    def as_list_of_dicts(self) -> List[dict]:
        return [parameter.as_dict() for parameter in self.__parameters]


class ParameterValue:
    """
    Containing one Value for a KPI or Design
    """

    def __init__(self, id: str, value: float):
        self.__id = id
        self.__value = value

    def get_id(self) -> str:
        return self.__id

    def get_value(self) -> float:
        return self.__value

    def as_dict(self) -> dict:
        return {"id": self.get_id(), "value": self.get_value()}

    @classmethod
    def from_dict(cls, from_dict: dict) -> ParameterValue:
        return cls(id=from_dict["id"], value=from_dict["value"])


class ParameterValues:
    """
    Containing a list of values
    """

    def __init__(self, values: List[ParameterValue]):
        self.__values = values

    def __iter__(self) -> Iterator[ParameterValue]:
        return iter(self.get_values())

    def get_values(self) -> List[ParameterValue]:
        return self.__values

    def get_value(self, id: str) -> float:
        searched_value = next(
            (value for value in self.__values if value.get_id() == id), None
        )

        if searched_value is None:
            raise ValueError(f"There is no Value for id '{id}'")

        return searched_value.get_value()

    def as_list_of_dicts(self) -> List[dict]:
        return [parameter_value.as_dict() for parameter_value in self.__values]

    @classmethod
    def from_list_of_dicts(cls, list_of_dicts: List[dict]) -> ParameterValues:
        return cls([ParameterValue.from_dict(list_dict) for list_dict in list_of_dicts])
