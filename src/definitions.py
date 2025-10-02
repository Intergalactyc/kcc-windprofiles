from windprofiles import (
    Location,
    TerrainClassifier,
    StabilityClassifier,
)

# Location of KCC met tower
LOCATION = Location(
    latitude=41.90919,
    longitude=-91.65505,
    elevation=256.5443,
    timezone="America/Chicago",
)

SOURCE_TIMEZONE = "UTC"

SOURCE_UNITS = {
    "p" : "mmHg",
    "t" : "C",
    "rh" : "%",
    "ws" : "m/s",
    "wd" : ("degrees", "W", "CW") #"degCW-W",
}

TOWER_HEIGHT = 106.

TERRAIN_WINDOW_WIDTH_DEGREES = 60.

REMOVAL_PERIODS = {
    (
        "2018-03-05 13:20:00",
        "2018-03-10 00:00:00",
    ): "ALL",  # large maintenance gap
    ("2018-04-18 17:40:00", "2018-04-19 14:20:00"): [
        6
    ],  # small maintenance-shaped gap
    (
        "2018-09-10 12:00:00",
        "2018-09-20 12:00:00",
    ): "ALL",  # blip at end
} # Manually-defined periods of unreliable data to rbe removed

# Define 4-class bulk Richardson number stability classification scheme
STABILITY_CLASSIFIER = StabilityClassifier(
    parameter="Ri_bulk",
    classes=[
        ("unstable", "(-inf,-0.1)"),
        ("neutral", "[-0.1,0.1)"),
        ("stable", "[0.1,0.25)"),
        ("strongly stable", "[0.25,inf)"),
    ],
)

# Define the terrain classification scheme
TERRAIN_CLASSIFIER = TerrainClassifier(
    complexCenter=315,
    openCenter=135,
    radius=60/2,
    inclusive=True,
    boom=2,
)

# All heights (in m) that data exists at
# Data columns follow "{type}_{boom}" format
HEIGHT_LIST = [6., 10., 20., 32., 80., 106.]
BOOM_LIST = [1, 2, 3, 4, 5, 6]
HEIGHTS = {b : h for b, h in zip(BOOM_LIST, HEIGHT_LIST)}

CID_UNITS = {
        "p" : "mBar_247asl",
        "t" : "C",
        "rh" : "%",
        "ws" : "mph",
        "wd" : ["degrees", "N", "CW"],
}

if __name__ == "__main__":
    from windprofiles.meteostat import get_weather_data
    from datetime import datetime

    data = get_weather_data(
        LOCATION, (datetime(2018, 1, 1), datetime(2019, 1, 1)), "daily"
    )
    print(data)
