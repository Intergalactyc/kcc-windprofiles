import os
import pandas as pd


def load_data(parent: str, outer_merges: bool = False):
    # Read in the data from the booms and set column names to common format
    boom1 = pd.read_csv(os.path.join(parent, "Boom1OneMin")).rename(
        columns={
            "TimeStamp": "time",
            "MeanVelocity (m/s)": "ws_1",
            "MeanDirection": "wd_1",
            "MeanTemperature (C )": "t_1",
            "MeanPressure (mmHg)": "p_1",
        }
    )

    boom2 = pd.read_csv(os.path.join(parent, "Boom1OneMin")).rename(
        columns={
            "TIMESTAMP": "time",
            "MeanVelocity (m/s)": "ws_2",
            "MeanDirection": "wd_2",
            "MeanTemperature (C )": "t_2",
            "MeanRH (%)": "rh_2",
        }
    )

    boom3 = pd.read_csv(os.path.join(parent, "Boom1OneMin")).rename(
        columns={
            "TIMESTAMP": "time",
            "MeanVelocity (m/s)": "ws_3",
            "MeanDirection": "wd_3",
        }
    )

    boom4 = pd.read_csv(os.path.join(parent, "Boom1OneMin")).rename(
        columns={
            "TimeStamp": "time",
            "MeanVelocity": "ws_4",
            "MeanDirection": "wd_4",
            "MeanTemperature": "t_4",
            "MeanRH": "rh_4",
        }
    )

    boom5 = pd.read_csv(os.path.join(parent, "Boom1OneMin")).rename(
        columns={
            "TimeStamp": "time",
            "MeanVelocity": "ws_5",
            "MeanDirection": "wd_5",
            "MeanTemperature": "t_5",
            "MeanRH": "rh_5",
        }
    )

    boom6 = pd.read_csv(os.path.join(parent, "Boom1OneMin")).rename(
        columns={
            "TIMESTAMP": "time",
            "MeanVelocity (m/s)": "ws_6a",
            "Mean Direction": "wd_6a",
            "MeanTemperature (C )": "t_6",
            "MeanRH (%)": "rh_6",
        }
    )

    boom7 = pd.read_csv(os.path.join(parent, "Boom1OneMin")).rename(
        columns={
            "TimeStamp": "time",
            "MeanVelocity (m/s)": "ws_6b",
            "MeanDirection": "wd_6b",
            "MeanPressure (mmHg)": "p_6",
        }
    )

    # Merge the data together into one pd.DataFrame
    boom_list = [boom1, boom2, boom3, boom4, boom5, boom6, boom7]
    for boom in boom_list:
        boom["time"] = pd.to_datetime(boom["time"])
        boom.set_index("time", inplace=True)
    df = (
        boom1.merge(boom2, on="time", how="outer" if outer_merges else "inner")
        .merge(boom6, on="time", how="outer" if outer_merges else "inner")
        .merge(boom7, on="time", how="outer" if outer_merges else "inner")
        .merge(boom3, on="time", how="outer" if outer_merges else "left")
        .merge(boom4, on="time", how="outer" if outer_merges else "left")
        .merge(boom5, on="time", how="outer" if outer_merges else "left")
    )

    return df
