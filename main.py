from extract import get_airlines, get_aircraft_types, get_destinations
from save import save
from transform import transform_airlines, transform_aircraft_types, transform_destinations
from pathlib import Path
import os


BASE_DIR = os.path.dirname(__file__)
SAVE_DIR = os.path.join(BASE_DIR, "data")


def main_etl():
    # extract
    airlines_pages = get_airlines()
    aircraft_types_pages = get_aircraft_types()
    destinations_pages = get_destinations()

    # transform
    airlines = transform_airlines(airlines_pages)
    aircraft_types = transform_aircraft_types(aircraft_types_pages)
    destinations = transform_destinations(destinations_pages)


    # load
    save(
        SAVE_DIR,
        [
            airlines,
            aircraft_types,
            destinations
        ],
        [
            "airlines",
            "aircraft_types",
            "destinations"
        ]
    )


    return 0


if __name__ == "__main__":
    main_etl()

