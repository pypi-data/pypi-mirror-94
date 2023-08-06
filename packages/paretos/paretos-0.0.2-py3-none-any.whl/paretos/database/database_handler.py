import uuid

import sqlalchemy_utils
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

from paretos.objects.enums import (
    ParameterOptions,
    ParameterTypes,
    ProjectStatusEnum,
    SimulationStatusEnum,
)

# import package models namespaced to avoid conflicts
from .. import objects as o
from ..exceptions import InitializationError
from .data_model import (
    DB_VERSION,
    Base,
    Parameter,
    ParameterOption,
    ParameterOptionType,
    ParameterType,
    ParameterValue,
    Project,
    ProjectStatus,
    Simulation,
    SimulationStatus,
    Version,
)
from ..objects.analyzed_results import AnalyzedEvaluations


class DB(object):
    """
    Class to connect database and get / post values
    """

    def __init__(self, database_path):
        database_url = f"sqlite:///{database_path}"
        create_database = not sqlalchemy_utils.database_exists(database_url)

        self.__engine = create_engine(database_url)

        if create_database:
            Base.metadata.create_all(self.__engine)

        session = sessionmaker(bind=self.__engine)
        self.__session = session()

        if not create_database and not self.__is_current_version():
            raise InitializationError(
                "Current DB version incompatible. Change DB path."
            )

        if create_database:
            self.set_init_db_data()

    def set_init_db_data(self):
        version = Version(id=uuid.uuid4(), name=DB_VERSION)

        self.__session.add(version)

        for project_status in ProjectStatusEnum:
            ps = ProjectStatus(id=uuid.uuid4(), name=project_status.value)

            self.__session.add(ps)

        for parameter_option in ParameterOptions:
            ct = ParameterOptionType(id=uuid.uuid4(), name=parameter_option.value)

            self.__session.add(ct)

        for simulation_status in SimulationStatusEnum:
            ss = SimulationStatus(id=uuid.uuid4(), name=simulation_status.value)

            self.__session.add(ss)

        for parameter_type in ParameterTypes:
            pt = ParameterType(id=uuid.uuid4(), name=parameter_type.value)

            self.__session.add(pt)

        self.__session.commit()

    def __is_current_version(self):
        most_current_version = (
            self.__session.query(Version).order_by(desc(Version.time_created)).first()
        )

        return most_current_version.name == DB_VERSION

    def add_project(self, project_name: str):
        project = Project(
            id=uuid.uuid4(),
            # USE Enum here as well
            statusCodeId=self.__session.query(ProjectStatus)
            .filter(ProjectStatus.name == ProjectStatusEnum.initialized.name)
            .first()
            .id,
            name=project_name,
        )

        self.__session.add(project)
        self.__session.commit()

        return project.id

    def __get_db_parameter(self, parameter: o.Parameter):
        return Parameter(
            id=uuid.uuid4(),
            parameter_type_id=self.__session.query(ParameterType)
            .filter(ParameterType.name == parameter.get_type().name)
            .first()
            .id,
            name=parameter.get_id(),
        )

    def __get_db_parameter_value(
        self, parameter_value: o.ParameterValue
    ) -> ParameterValue:
        parameter_value_id = uuid.uuid4()
        parameter_id = (
            self.__session.query(Parameter)
            .filter(Parameter.name == parameter_value.get_id())
            .first()
            .id
        )
        value = parameter_value.get_value()

        return ParameterValue(
            id=parameter_value_id,
            parameter_id=parameter_id,
            number_value=value,
        )

    def add_project_meta(self, project_id: str, problem: o.OptimizationProblem):
        project = self.__session.query(Project).filter(Project.id == project_id).first()

        for design_param in problem.get_design_space():
            design_db_param = self.__get_db_parameter(design_param)

            minimum = design_param.get_minimum()
            maximum = design_param.get_maximum()
            minimum_option = ParameterOption(
                id=uuid.uuid4(),
                parameter_option_type_id=self.__session.query(ParameterOptionType)
                .filter(ParameterOptionType.name == ParameterOptions.minimum.name)
                .first()
                .id,
                number_value=minimum,
            )

            design_db_param.options.append(minimum_option)

            maximum_option = ParameterOption(
                id=uuid.uuid4(),
                parameter_option_type_id=self.__session.query(ParameterOptionType)
                .filter(ParameterOptionType.name == ParameterOptions.maximum.name)
                .first()
                .id,
                number_value=maximum,
            )

            design_db_param.options.append(maximum_option)

            project.parameter.append(design_db_param)

        for kpi_param in problem.get_kpi_space():
            kpi_db_param = self.__get_db_parameter(kpi_param)

            goal = kpi_param.get_goal()

            goal_option = ParameterOption(
                id=uuid.uuid4(),
                parameter_option_type_id=self.__session.query(ParameterOptionType)
                .filter(ParameterOptionType.name == ParameterOptions.goal.name)
                .first()
                .id,
                string_value=goal.name,
            )

            kpi_db_param.options.append(goal_option)

            project.parameter.append(kpi_db_param)

        self.__session.commit()

    def add_simulation_design(self, project_id, design_values: o.DesignValues) -> str:
        simulation = Simulation(
            id=uuid.uuid4(),
            status_code_id=self.__session.query(SimulationStatus)
            .filter(SimulationStatus.name == SimulationStatusEnum.predicted.name)
            .first()
            .id,
            project_id=project_id,
            is_pareto=False,
        )

        for design_value in design_values:
            parameter_value = self.__get_db_parameter_value(design_value)
            simulation.values.append(parameter_value)

        self.__session.add(simulation)

        self.__session.commit()

        return simulation.id

    def _get_simulation_object(self, simulation_id: str):
        return (
            self.__session.query(Simulation)
            .filter(Simulation.id == simulation_id)
            .first()
        )

    def add_simulation_kpis(self, simulation_id: str, kpi_values: o.KpiValues) -> str:
        simulation = self._get_simulation_object(simulation_id)

        for kpi_value in kpi_values:
            parameter_value = self.__get_db_parameter_value(kpi_value)
            simulation.values.append(parameter_value)

            self.__session.commit()

        return simulation_id

    def get_all_simulation_data(self, project_id: str):
        raise NotImplementedError

    def get_project_meta(self, project_id: str) -> dict:
        # TODO: Adapt for new api version
        project = (
            self.__session.query(Project).filter(Project.id == project_id).scalar()
        )

        design = []
        kpis = []

        rows = (
            self.__session.query(ParameterOption, Parameter, ParameterOptionType)
            .join(ParameterOption, Parameter.options)
            .filter(
                Parameter.name.in_(
                    [
                        a.name
                        for a in self.__session.query(Project)
                        .filter(Project.id == project_id)
                        .scalar()
                        .parameter
                    ]
                )
            )
            .filter(
                ParameterOptionType.name == ParameterOptions.maximum
                or ParameterOptionType.name == ParameterOptions.minimum
            )
            .all()
        )
        for c, p, ct in rows:
            design.append(
                {"id": p.name, "constraints": [{"type": ct.name, "value": c.value}]}
            )

        for parameter in project.parameter:
            if (
                self.__session.query(ParameterType)
                .filter(ParameterType.id == parameter.parameterTypeCode)
                .scalar()
                .name
                == "kpi"
            ):
                kpis.append(parameter.name)

        return {"design": design, "kpis": kpis}

    def update_pareto_state(self, analyzed_result: AnalyzedEvaluations):
        pareto_ids = analyzed_result.get_pareto_evaluations()

        for pareto_id in pareto_ids:
            simulation = self._get_simulation_object(pareto_id)
            simulation.is_pareto = True

            self.__session.add(simulation)

        self.__session.commit()
