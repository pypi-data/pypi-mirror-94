import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    String,
    Table,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import CHAR, TypeDecorator

DB_VERSION = "db_version_1"

Base = declarative_base()

# TODO: Check for correct relationships with documentation

"""
Note: The highlighting issues are a Problem of Pycharm with multiple Base classes
Best practice https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/mixins.html
alternative is to extend base class what leads to unnecessary columns in relationship
tables. :(
"""


class TimedTable:
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """

    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


project_parameters = Table(
    "project_parameters",
    Base.metadata,
    Column("project_id", GUID, ForeignKey("project.id")),
    Column("parameter_id", GUID, ForeignKey("parameter.id")),
)

simulation_values = Table(
    "simulation_values",
    Base.metadata,
    Column("simulation_id", GUID, ForeignKey("simulation.id")),
    Column("parameter_value_id", GUID, ForeignKey("parameter_value.id")),
)


class Project(TimedTable, Base):
    __tablename__ = "project"

    id = Column(
        GUID(), primary_key=True, nullable=False, unique=True, default=str(uuid.uuid4())
    )

    statusCodeId = Column(GUID, ForeignKey("project_status.id"))

    name = Column(String)

    simulation = relationship("Simulation")

    parameter = relationship(
        "Parameter",
        secondary=project_parameters,
    )


class Simulation(TimedTable, Base):
    __tablename__ = "simulation"

    id = Column(
        GUID(), primary_key=True, nullable=False, unique=True, default=str(uuid.uuid4())
    )

    status_code_id = Column(GUID, ForeignKey("simulation_status.id"))

    project_id = Column(GUID, ForeignKey("project.id"))

    is_pareto = Column(Boolean)

    values = relationship(
        "ParameterValue",
        secondary=simulation_values,
    )


class SimulationStatus(TimedTable, Base):
    __tablename__ = "simulation_status"

    id = Column(
        GUID(), primary_key=True, nullable=False, unique=True, default=str(uuid.uuid4())
    )

    name = Column(String)

    simulation = relationship("Simulation")


class Parameter(TimedTable, Base):
    __tablename__ = "parameter"

    id = Column(
        GUID(), primary_key=True, nullable=False, unique=True, default=str(uuid.uuid4())
    )

    parameter_type_id = Column(GUID, ForeignKey("parameter_type.id"))

    name = Column(String)

    unit = Column(String)

    options = relationship("ParameterOption", back_populates="parameter")

    type = relationship("ParameterType", back_populates="parameter")

    value = relationship("ParameterValue", back_populates="parameter")


class ParameterType(TimedTable, Base):
    __tablename__ = "parameter_type"

    id = Column(
        GUID(), primary_key=True, nullable=False, unique=True, default=str(uuid.uuid4())
    )

    name = Column(String)

    parameter = relationship("Parameter", back_populates="type")


class ParameterValue(TimedTable, Base):
    __tablename__ = "parameter_value"

    id = Column(
        GUID(), primary_key=True, nullable=False, unique=True, default=str(uuid.uuid4())
    )

    parameter_id = Column(GUID, ForeignKey("parameter.id"))

    number_value = Column(Float)

    parameter = relationship("Parameter", back_populates="value")


class ProjectStatus(TimedTable, Base):
    __tablename__ = "project_status"

    id = Column(
        GUID(), primary_key=True, nullable=False, unique=True, default=str(uuid.uuid4())
    )

    name = Column(String)

    project = relationship("Project")


class ParameterOption(TimedTable, Base):
    __tablename__ = "parameter_option"

    id = Column(
        GUID(), primary_key=True, nullable=False, unique=True, default=str(uuid.uuid4())
    )

    parameter_option_type_id = Column(GUID, ForeignKey("parameter_option_type.id"))

    parameter_id = Column(GUID, ForeignKey("parameter.id"))

    number_value = Column(Float)
    string_value = Column(String)

    type = relationship("ParameterOptionType", back_populates="option")

    parameter = relationship("Parameter", back_populates="options")


class ParameterOptionType(TimedTable, Base):
    __tablename__ = "parameter_option_type"

    id = Column(
        GUID(), primary_key=True, nullable=False, unique=True, default=str(uuid.uuid4())
    )

    name = Column(String, unique=True)

    option = relationship("ParameterOption", back_populates="type")


class Version(TimedTable, Base):
    __tablename__ = "version"

    id = Column(
        GUID(), primary_key=True, nullable=False, unique=True, default=str(uuid.uuid4())
    )

    name = Column(String, unique=True)
