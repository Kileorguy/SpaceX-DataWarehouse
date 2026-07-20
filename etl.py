from etl.config import TABLE_CONFIG, FACT_CONFIG
from etl.generic_loader import load_dimension, load_fact
from etl.lookups import build_lookups

def run():

    for model, config in TABLE_CONFIG.items():
        load_dimension(

            model=model,

            json_file=config["json_file"],

            unique_key=config["unique_key"],

            transform=config["transform"]
        )

    lookups = build_lookups()
    # print(lookups)

    for model, cfg in FACT_CONFIG.items():

        load_fact(
            model=model,
            json_file=cfg[
                "json_file"
            ],
            unique_key=cfg[
                "unique_key"
            ],
            transform=cfg[
                "transform"
            ],
            lookups=lookups
        )


if __name__ == "__main__":

    run()