from extract import get_airlines
from save import save
from transform import transform_airlines
from pathlib import Path
import os


BASE_DIR = os.path.dirname(__file__)
SAVE_DIR = os.path.join(BASE_DIR, "data")


def main_etl():
    # extract
    airlines_pages = get_airlines()


    # transform
    airlines = transform_airlines(airlines_pages)
    
    # load
    save(
        SAVE_DIR,
        [
            airlines
        ],
        [
            "airlines"
        ]
    )


    return 0


if __name__ == "__main__":
    main_etl()

