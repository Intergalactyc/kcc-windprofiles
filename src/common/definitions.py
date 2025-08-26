from windprofiles import Location

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
        "wd" : "degCW-W",
}

TOWER_HEIGHT = 106.

TERRAIN_WINDOW_WIDTH_DEGREES = 60.

if __name__ == "__main__":
    from windprofiles.meteostat import get_weather_data
    from datetime import datetime

    data = get_weather_data(
        LOCATION, (datetime(2018, 1, 1), datetime(2019, 1, 1)), "daily"
    )
    print(data)
