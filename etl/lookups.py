from database import SessionLocal

from models import *


def make_lookup(
    db,
    model,
    business_key,
    surrogate_key
):
    return {
        str(getattr(row, business_key)): getattr(row, surrogate_key)
        for row in db.query(model).all()
    }


def build_lookups():

    db = SessionLocal()

    try:

        return {

            "date": make_lookup(
                db,
                DateDimension,
                "date_key",
                "date_key"
            ),

            "rocket": make_lookup(
                db,
                RocketDimension,
                "rocket_id",
                "rocket_key"
            ),

            "mission": make_lookup(
                db,
                MissionDimension,
                "mission_id",
                "mission_key"
            ),

            "pad": make_lookup(
                db,
                PadDimension,
                "pad_id",
                "pad_key"
            ),

            "status": make_lookup(
                db,
                StatusDimension,
                "status_id",
                "status_key"
            ),

            "provider": make_lookup(
                db,
                ProviderDimension,
                "provider_id",
                "provider_key"
            ),
            "spacecraft": make_lookup(
                db,
                SpacecraftDimension,
                "spacecraft_id",
                "spacecraft_key"
            ),

            "location": make_lookup(
                db,
                LocationDimension,
                "location_id",
                "location_key"
            ),

            "landing_type": make_lookup(
                db,
                LandingTypeDimension,
                "landing_type_id",
                "landing_type_key"
            ),

            "program": make_lookup(
                db,
                ProgramDimension,
                "program_id",
                "program_key"
            ),

            "agency": make_lookup(
                db,
                AgencyDimension,
                "agency_id",
                "agency_key"
            ),

            "launch": make_lookup(
                db,
                LaunchFact,
                "launch_key",
                "launch_key"
            ),
        }

    finally:

        db.close()