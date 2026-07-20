from config import TABLE_CONFIG
from generic_loader import load_dimension


def run():

    for model, config in TABLE_CONFIG.items():

        load_dimension(

            model=model,

            json_file=config["json_file"],

            unique_key=config["unique_key"],

            transform=config["transform"]
        )


if __name__ == "__main__":

    run()