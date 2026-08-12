from models import *
from datetime import datetime

TABLE_CONFIG = {

    # ==========================
    # DIMENSIONS
    # ==========================

    RocketDimension: {

        "json_file": "staging_data/splitted/rockets.json",

        "unique_key": "rocket_id",

        "transform": lambda x: {

            "rocket_id": x["id"],

            "name": x["name"],

            "variant": x["variant"],

            "family": x["families"][0]["name"] if x["families"] else None
        }
    },

    MissionDimension: {
    
        "json_file": "staging_data/splitted/missions.json",
    
        "unique_key": "mission_id",
    
        "transform": lambda x: {
    
            "mission_id": x["id"],
    
            "mission_name": x["name"],
    
            "mission_type": x["type"],
    
            "mission_description": x["description"]
        }
    },
    
    PadDimension: {
    
        "json_file": "staging_data/splitted/pads.json",
    
        "unique_key": "pad_id",
    
        "transform": lambda x: {
    
            "pad_id": x["id"],
    
            "pad_name": x["name"],
    
            "location_name": x["location"]["name"],
    
            "country": x["location"]["country"]["name"],
    
            "active": x["active"]
        }
    },

    StatusDimension: {
    
        "json_file": "staging_data/splitted/launches.json",
    
        "unique_key": "status_id",
    
        "transform": lambda x: {
    
            "status_id": x["status"]["id"],
    
            "status_name": x["status"]["name"],
    
            "abbreviation": x["status"]["abbrev"],
    
            "description": x["status"]["description"]
        }
    },

    ProviderDimension: {
    
        "json_file": "staging_data/splitted/providers.json",
    
        "unique_key": "provider_id",
    
        "transform": lambda x: {
    
            "provider_id": x["id"],
    
            "provider_name": x["name"],
    
            "abbreviation": x["abbrev"],
    
            "agency_type": x["type"]["name"]
        }
    },
    
    DateDimension: {
    
    "json_file": "staging_data/splitted/launches.json",
    
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
            x["window_start"].replace("Z", "+00:00")
        )
    ),
    },

    LandingTypeDimension: {
    
        "json_file": "staging_data/splitted/landings.json",
    
        "unique_key": "landing_type_id",
    
        "transform": lambda x: {
    
            "landing_type_id": x['type']['id'],
    
            "landing_type_name": x['type']['name'],
    
            "abbreviation": x['type']['abbrev'],
    
            "description": x['type']['description']
        }
    },

    LocationDimension: {
    
        "json_file": "staging_data/splitted/landings.json",
    
        "unique_key": "location_id",
    
        "transform": lambda x: {
            "location_id": x['landing_location']["id"] if x['landing_location'] else None,
            "name": x['landing_location']['name'] if x['landing_location'] else None,
    
            "abbreviation": x['landing_location']['abbrev'] if x['landing_location'] else None,
    
            "description": x['landing_location']['description'] if x['landing_location'] else None,
    
            "latitude": x['landing_location']['latitude'] if x['landing_location'] else None,
    
            "longitude": x['landing_location']['longitude'] if x['landing_location'] else None
        }
    },

    SpacecraftDimension: {
    
        "json_file": "staging_data/splitted/spacecrafts.json",
    
        "unique_key": "spacecraft_id",
    
        "transform": lambda x: None if x is None else {
    
            "spacecraft_id": x['id'],
    
            "spacecraft_name": x['name'],
    
            "serial_number": x['serial_number'],
    
            "configuration_name": x['spacecraft_config']['name'],
    
            "spacecraft_type": x['spacecraft_config']['type']['name'],
    
            "status": x['status']['name'],
    
            "in_use": x['in_space'],
    
            "lifetime_flights": x['flights_count'],
    
            "description": x['description']
        }
    },
    
    ProgramDimension: {
    
        "json_file": "staging_data/splitted/programs.json",
    
        "unique_key": "program_id",
    
        "transform": lambda x: [
    
            {
                "program_id": x["id"],
                "program_name": x["name"]
            }
            
        ]
    },

    AgencyDimension: {
    
        "json_file": "staging_data/splitted/agencies.json",
    
        "unique_key": "agency_id",
    
        "transform": lambda x: {
    
            "agency_id": x['id'],
    
            "agency_name": x['name'],
    
            "abbreviation": x['abbrev'],
    
            "agency_type": x['type']['name'],
    
            "country": x['country'][0]['name'],
    
            "administrator": x['administrator']
        }
    },

    OrbitDimension: {
        "json_file": "staging_data/splitted/orbits.json",

        "unique_key": "orbit_id",

        "transform": lambda x: {
            "orbit_id": x.get("id"),
            "name": x.get("name")
        }
},

}

FACT_CONFIG = {

    LaunchFact: {

    "json_file": "staging_data/splitted/launches.json",

    "unique_key": "launch_key",

    "transform": lambda x, lookup: {

        "launch_key": x["id"],
        "orbit_key": x["mission"]["orbit"]["id"], 

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

    "json_file": "staging_data/splitted/landings.json",

    "unique_key": "landing_id",

    "transform": lambda x, lookup: {

        "landing_id": x["id"],
        "orbit_key": x["spacecraftflight"]["launch"]["mission"]["orbit"]["id"] if x["spacecraftflight"] else None,

        "date_key": lookup["date"][
            str(int(
                datetime
                .fromisoformat(
                    x["spacecraftflight"]["launch"]["window_start"]
                    .replace(
                        "Z",
                        "+00:00"
                    )
                )
                .strftime("%Y%m%d")
            )) 
        ]  if x["spacecraftflight"] else None,

        "spacecraft_key": lookup[
            "spacecraft"
        ][
            str(
                int(x["spacecraft_id"])
            )
        ] if x["spacecraft_id"] else None,

        "location_key": lookup[
            "location"
        ][
            str(
                x["landing_location"]["id"]
            )
        ] if x["landing_location"] else None,

        "landing_type_key": lookup[
            "landing_type"
        ][
            str(
                x["type"]["id"]
            )
        ],

        "attempt_flag": x["attempt"],

        "success_flag": x["success"]
    }
},
PayloadFact: {

    "json_file": "staging_data/splitted/payloads.json",

    "unique_key": "payload_id",

    "transform": lambda x, lookup: {

        "payload_id": x["id"],
        "payload_name": x["name"],
        "description": x["description"],
        "payload_type": x["type"]["id"],

        "launch_key": None,
        # lookup[ UDAH GA DIPAKE
        #     "launch"
        # ].get(
        #     str(pr
        #         x["launch"]["id"]
        #     )
        # ),

        "program_key": (
            lookup["program"].get(
                str(x["program"][0]["id"])
            )
            if x["program"]
            else None
        ),

        "manufacturer_key": lookup[
            "agency"
        ][
            str(
                x["manufacturer"]["id"]
            )
        ],

        "operator_key": lookup[
            "agency"
        ][
            str(
                x["operator"]["id"]
            )
        ],

        "payload_count": 1,

        "mass_kg": x["mass"],

        "cost": x["cost"] or -1
    }
}

    
}