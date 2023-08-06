from ..objects.design import DesignValues
from ..objects.kpi import KpiValues


class Environment:
    """Interface to describe Environments"""

    def simulate(self, design_values: DesignValues) -> KpiValues:
        """
        Function which wraps the model to be modified and evaluated on performance
        :param design_values: List of dicts containing a design parameters each
        :return: List of dicts containing the matching kpis
        """
        raise NotImplementedError
