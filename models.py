from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    Text,
    Date,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database import Base


# ==========================
# DIMENSIONS
# ==========================

class DateDimension(Base):
    __tablename__ = "dim_date"

    date_key = Column(Integer, primary_key=True)

    full_date = Column(Date, nullable=False)
    year = Column(Integer)
    quarter = Column(Integer)
    month = Column(Integer)
    week = Column(Integer)
    day = Column(Integer)


class RocketDimension(Base):
    __tablename__ = "dim_rocket"

    rocket_key = Column(Integer, primary_key=True)

    rocket_id = Column(String, unique=True)
    name = Column(String)
    variant = Column(String)
    family = Column(String)


class PadDimension(Base):
    __tablename__ = "dim_pad"

    pad_key = Column(Integer, primary_key=True)

    pad_id = Column(String, unique=True)
    pad_name = Column(String)
    location_name = Column(String)
    country = Column(String)
    active = Column(Boolean)


class MissionDimension(Base):
    __tablename__ = "dim_mission"

    mission_key = Column(Integer, primary_key=True)

    mission_id = Column(String, unique=True)
    mission_name = Column(String)
    mission_type = Column(String)
    mission_description = Column(Text)


class StatusDimension(Base):
    __tablename__ = "dim_status"

    status_key = Column(Integer, primary_key=True)

    status_id = Column(Integer, unique=True)
    status_name = Column(String)
    abbreviation = Column(String)
    description = Column(Text)


class ProviderDimension(Base):
    __tablename__ = "dim_provider"

    provider_key = Column(Integer, primary_key=True)

    provider_id = Column(String, unique=True)
    provider_name = Column(String)
    abbreviation = Column(String)
    agency_type = Column(String)


class LocationDimension(Base):
    __tablename__ = "dim_location"

    location_key = Column(Integer, primary_key=True)

    name = Column(String)
    abbreviation = Column(String)
    description = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)


class LandingTypeDimension(Base):
    __tablename__ = "dim_landing_type"

    landing_type_key = Column(Integer, primary_key=True)

    landing_type_id = Column(String)
    landing_type_name = Column(String)
    abbreviation = Column(String)
    description = Column(Text)


class SpacecraftDimension(Base):
    __tablename__ = "dim_spacecraft"

    spacecraft_key = Column(Integer, primary_key=True)

    spacecraft_id = Column(String, unique=True)
    spacecraft_name = Column(String)
    serial_number = Column(String)
    configuration_name = Column(String)
    spacecraft_type = Column(String)
    status = Column(String)
    in_use = Column(Boolean)
    lifetime_flights = Column(Integer)
    description = Column(Text)


class SpaceStationDimension(Base):
    __tablename__ = "dim_space_station"

    space_station_key = Column(Integer, primary_key=True)

    space_station_id = Column(String)
    station_name = Column(String)
    status = Column(String)
    orbit = Column(String)
    station_type = Column(String)
    description = Column(Text)


class ProgramDimension(Base):
    __tablename__ = "dim_program"

    program_key = Column(Integer, primary_key=True)

    program_id = Column(String)
    program_name = Column(String)


class AgencyDimension(Base):
    __tablename__ = "dim_agency"

    agency_key = Column(Integer, primary_key=True)

    agency_id = Column(String)
    agency_name = Column(String)
    abbreviation = Column(String)
    agency_type = Column(String)
    country = Column(String)
    administrator = Column(String)


# ==========================
# FACT TABLES
# ==========================

class LaunchFact(Base):
    __tablename__ = "fact_launch"

    launch_key = Column(Integer, primary_key=True)

    date_key = Column(
        Integer,
        ForeignKey("dim_date.date_key")
    )

    rocket_key = Column(
        Integer,
        ForeignKey("dim_rocket.rocket_key")
    )

    mission_key = Column(
        Integer,
        ForeignKey("dim_mission.mission_key")
    )

    pad_key = Column(
        Integer,
        ForeignKey("dim_pad.pad_key")
    )

    status_key = Column(
        Integer,
        ForeignKey("dim_status.status_key")
    )

    provider_key = Column(
        Integer,
        ForeignKey("dim_provider.provider_key")
    )

    launch_count = Column(Integer, default=1)

    success = Column(Boolean)


class LandingFact(Base):
    __tablename__ = "fact_landing"

    landing_fact_key = Column(Integer, primary_key=True)

    landing_id = Column(String)

    date_key = Column(
        Integer,
        ForeignKey("dim_date.date_key")
    )

    location_key = Column(
        Integer,
        ForeignKey("dim_location.location_key")
    )

    landing_type_key = Column(
        Integer,
        ForeignKey("dim_landing_type.landing_type_key")
    )

    spacecraft_key = Column(
        Integer,
        ForeignKey("dim_spacecraft.spacecraft_key")
    )

    attempt_flag = Column(Boolean)

    success_flag = Column(Boolean)


class PayloadFact(Base):
    __tablename__ = "fact_payload"

    payload_fact_key = Column(Integer, primary_key=True)

    payload_id = Column(String)

    payload_name = Column(String)

    description = Column(Text)

    payload_type = Column(String)

    manufacturer_key = Column(
        Integer,
        ForeignKey("dim_agency.agency_key")
    )

    operator_key = Column(
        Integer,
        ForeignKey("dim_agency.agency_key")
    )

    program_key = Column(
        Integer,
        ForeignKey("dim_program.program_key")
    )

    launch_key = Column(
        Integer,
        ForeignKey("fact_launch.launch_key")
    )

    payload_count = Column(Integer)

    mass_kg = Column(Float)

    cost = Column(Float)