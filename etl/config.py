from models import *
from datetime import datetime

TABLE_CONFIG = {

    # ==========================
    # DIMENSIONS
    # ==========================

    RocketDimension: {

        "json_file": "staging_data/launches.json",

        "unique_key": "rocket_id",

        "transform": lambda x: {

            "rocket_id": x["rocket"]["id"],

            "name": x["rocket"]["configuration"]["name"],

            "variant": x["rocket"]["configuration"]["variant"],

            "family": x["rocket"]["configuration"]["families"][0]["name"]
        }
    },

    MissionDimension: {

        "json_file": "staging_data/launches.json",

        "unique_key": "mission_id",

        "transform": lambda x: {

            "mission_id": x["mission"]["id"],

            "mission_name": x["mission"]["name"],

            "mission_type": x["mission"]["type"],

            "mission_description": x["mission"]["description"]
        }
    },

    PadDimension: {

        "json_file": "staging_data/launches.json",

        "unique_key": "pad_id",

        "transform": lambda x: {

            "pad_id": x["pad"]["id"],

            "pad_name": x["pad"]["name"],

            "location_name": x["pad"]["location"]["name"],

            "country": x["pad"]["location"]["country"]["name"],

            "active": x["pad"]["active"]
        }
    },

    StatusDimension: {

        "json_file": "staging_data/launches.json",

        "unique_key": "status_id",

        "transform": lambda x: {

            "status_id": x["status"]["id"],

            "status_name": x["status"]["name"],

            "abbreviation": x["status"]["abbrev"],

            "description": x["status"]["description"]
        }
    },

    ProviderDimension: {

        "json_file": "staging_data/launches.json",

        "unique_key": "provider_id",

        "transform": lambda x: {

            "provider_id": x["launch_service_provider"]["id"],

            "provider_name": x["launch_service_provider"]["name"],

            "abbreviation": x["launch_service_provider"]["abbrev"],

            "agency_type": x["launch_service_provider"]["type"]["name"]
        }
    },

    DateDimension: {

    "json_file": "staging_data/spacecraft_flights.json",

    "unique_key": "date_key",

    "transform": lambda x: (

        lambda dt: {

            "date_key": int(dt.strftime("%Y%m%d")),

            "full_date": dt.date(),

            "year": dt.year,

            "quarter": (dt.month - 1) // 3 + 1,

            "month": dt.month,

            "week": dt.isocalendar().week,

            "day": dt.day

        }

    )(
        datetime.fromisoformat(
            x["launch"]["window_start"].replace("Z", "+00:00")
            # x["launch"]["window_end"].replace("Z", "+00:00")
        )
    ),
    },

    DateDimension: {

    "json_file": "staging_data/launches.json",

    "unique_key": "date_key",

    "transform": lambda x: (

        lambda dt: {

            "date_key": int(dt.strftime("%Y%m%d")),

            "full_date": dt.date(),

            "year": dt.year,

            "quarter": (dt.month - 1) // 3 + 1,

            "month": dt.month,

            "week": dt.isocalendar().week,

            "day": dt.day

        }

    )(
        datetime.fromisoformat(
            x["window_end"].replace("Z", "+00:00")
            # x["window_start"].replace("Z", "+00:00")
        )
    ),
    },
    

    LandingTypeDimension: {

        "json_file": "staging_data/landings.json",

        "unique_key": "landing_type_id",

        "transform": lambda x: {

            "landing_type_id": x['type']['id'],

            "landing_type_name": x['type']['name'],

            "abbreviation": x['type']['abbrev'],

            "description": x['type']['description']
        }
    },

    LocationDimension: {

        "json_file": "staging_data/spacecraft_flights.json",

        "unique_key": "location_id",

        "transform": lambda x: {

            "location_id": x['landing']['landing_location']["id"],

            "name": x['landing']['landing_location']['name'],

            "abbreviation": x['landing']['landing_location']['abbrev'],

            "description": x['landing']['landing_location']['description'],

            "latitude": x['landing']['landing_location']['latitude'],

            "longitude": x['landing']['landing_location']['longitude']
        }
    },

    SpacecraftDimension: {

        "json_file": "staging_data/spacecraft_flights.json",

        "unique_key": "spacecraft_id",

        "transform": lambda x: None if x.get("spacecraft") is None else {

            "spacecraft_id": x['spacecraft']['id'],

            "spacecraft_name": x['spacecraft']['name'],

            "serial_number": x['spacecraft']['serial_number'],

            "configuration_name": x['spacecraft']['spacecraft_config']['name'],

            "spacecraft_type": x['spacecraft']['spacecraft_config']['type']['name'],

            "status": x['spacecraft']['status']['name'],

            "in_use": x['spacecraft']['in_space'],

            "lifetime_flights": x['spacecraft']['flights_count'],

            "description": x['spacecraft']['description']
        }
    },

    ProgramDimension: {

        "json_file": "staging_data/payload_flights.json",

        "unique_key": "program_id",

        "transform": lambda x: [

            {
                "program_id": program["id"],
                "program_name": program["name"]
            }

            for program in x["payload"]["program"]
        ]
    },

    AgencyDimension: {

        "json_file": "staging_data/payload_flights.json",

        "unique_key": "agency_id",

        "transform": lambda x: {

            "agency_id": x['payload']['manufacturer']['id'],

            "agency_name": x['payload']['manufacturer']['name'],

            "abbreviation": x['payload']['manufacturer']['abbrev'],

            "agency_type": x['payload']['manufacturer']['type']['name'],

            "country": x['payload']['manufacturer']['country'][0]['name'],

            "administrator": x['payload']['manufacturer']['administrator']
        }
    },

    AgencyDimension: {

        "json_file": "staging_data/payload_flights.json",

        "unique_key": "agency_id",

        "transform": lambda x: {

            "agency_id": x['payload']['operator']['id'],

            "agency_name": x['payload']['operator']['name'],

            "abbreviation": x['payload']['operator']['abbrev'],

            "agency_type": x['payload']['operator']['type']['name'],

            "country": x['payload']['operator']['country'][0]['name'],

            "administrator": x['payload']['operator']['administrator']
        }
    },


    
}

FACT_CONFIG = {

    LaunchFact: {

    "json_file": "staging_data/launches.json",

    "unique_key": "launch_key",

    "transform": lambda x, lookup: {

        "launch_key": x["id"],

        "date_key": lookup["date"].get(
            int(
                datetime
                .fromisoformat(
                    x["window_start"].replace("Z", "+00:00")
                )
                .strftime("%Y%m%d")
            )
        ),

        "rocket_key": lookup[
            "rocket"
        ][
            str(x["rocket"]["id"])
        ],

        "mission_key": lookup[
            "mission"
        ][
            str(x["mission"]["id"])
        ],

        "pad_key": lookup[
            "pad"
        ][
            str(x["pad"]["id"])
        ],

        "status_key": lookup[
            "status"
        ][
            str(x["status"]["id"])
        ],

        "provider_key": lookup[
            "provider"
        ][
            str(x[
                "launch_service_provider"
            ]["id"])
        ],

        "launch_count": x["location_launch_attempt_count"],

        "success": (
            x["status"]["name"]
            == "Launch Successful"
        )
    }
},
LandingFact: {

    "json_file": "staging_data/spacecraft_flights.json",

    "unique_key": "landing_id",

    "transform": lambda x, lookup: {

        "landing_id": x["landing"]["id"],

        "date_key": lookup["date"][
            str(int(
                datetime
                .fromisoformat(
                    x["launch"]["window_start"]
                    .replace(
                        "Z",
                        "+00:00"
                    )
                )
                .strftime("%Y%m%d")
            ))
        ],

        "spacecraft_key": lookup[
            "spacecraft"
        ][
            str(
                x["spacecraft"]["id"]
            )
        ],

        "location_key": lookup[
            "location"
        ][
            str(
                x["landing"]["landing_location"]["id"]
            )
        ],

        "landing_type_key": lookup[
            "landing_type"
        ][
            str(
                x["landing"]["type"]["id"]
            )
        ],

        "attempt_flag": x["landing"]["attempt"],

        "success_flag": x["landing"]["success"]
    }
},
PayloadFact: {

    "json_file": "staging_data/payload_flights.json",

    "unique_key": "payload_id",

    "transform": lambda x, lookup: {

        "payload_id": x["id"],
        "payload_name": x["payload"]["name"],
        "description": x["payload"]["description"],
        "payload_type": x["payload"]["type"]["id"],

        "launch_key": lookup[
            "launch"
        ].get(
            str(
                x["launch"]["id"]
            )
        ),

        "program_key": (
            lookup["program"].get(
                str(x["payload"]["program"][0]["id"])
            )
            if x["payload"]["program"]
            else None
        ),

        "manufacturer_key": lookup[
            "agency"
        ][
            str(
                x["payload"]["manufacturer"]["id"]
            )
        ],

        "operator_key": lookup[
            "agency"
        ][
            str(
                x["payload"]["operator"]["id"]
            )
        ],

        "payload_count": 1,

        "mass_kg": x['payload']["mass"],

        "cost": x["payload"]["cost"] or -1
    }
}

    
}