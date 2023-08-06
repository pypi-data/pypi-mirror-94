from enum import Enum


class ProjectStatusEnum(Enum):
    """
    Describing all available project status possibilities
    """

    initialized = "initialized"
    distributed = "distributed"
    set = "set"


class ParameterOptions(Enum):
    """
    Describing all available parameter options type
    """

    minimum = "minimum"
    maximum = "maximum"
    goal = "goal"


class SimulationStatusEnum(Enum):
    """
    Describing all available simulation status possibilities
    """

    predicted = "predicted"
    running = "running"
    completed = "completed"


class ParameterTypes(Enum):
    """
    Describing all available parameter type possibilities
    """

    design = "design"
    kpi = "kpi"


class Goals(Enum):
    """
    All possible goal options
    """

    minimize = "minimize"
    maximize = "maximize"


class RequestMethods(Enum):
    """
    All possible Request Methods
    """

    POST = "POST"
    GET = "GET"
