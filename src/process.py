# ruff: noqa: F403,F405

import pandas as pd
import windprofiles.process.qc as qc
import windprofiles.process.units as units
import windprofiles.process.format as fmt
import windprofiles.process.sampling as sampling
import windprofiles.process.compute as compute
import os
from definitions import *
from config import parse


SAVEDIR = os.path.join(os.path.abspath(__file__), "../results/processed")


def load_data(data_directory: str) -> pd.DataFrame:
    # Read in the data from the booms and set column names to common format
    boom1 = pd.read_csv(f"{data_directory}/Boom1OneMin.csv").rename(
        columns={
            "TimeStamp": "time",
            "MeanVelocity (m/s)": "ws_1",
            "MeanDirection": "wd_1",
            "MeanTemperature (C )": "t_1",
            "MeanPressure (mmHg)": "p_1",
        }
    )

    boom2 = pd.read_csv(f"{data_directory}/Boom2OneMin.csv").rename(
        columns={
            "TIMESTAMP": "time",
            "MeanVelocity (m/s)": "ws_2",
            "MeanDirection": "wd_2",
            "MeanTemperature (C )": "t_2",
            "MeanRH (%)": "rh_2",
        }
    )

    boom3 = pd.read_csv(f"{data_directory}/Boom3OneMin.csv").rename(
        columns={
            "TIMESTAMP": "time",
            "MeanVelocity (m/s)": "ws_3",
            "MeanDirection": "wd_3",
        }
    )

    boom4 = pd.read_csv(f"{data_directory}/Boom4OneMin.csv").rename(
        columns={
            "TimeStamp": "time",
            "MeanVelocity": "ws_4",
            "MeanDirection": "wd_4",
            "MeanTemperature": "t_4",
            "MeanRH": "rh_4",
        }
    )

    boom5 = pd.read_csv(f"{data_directory}/Boom5OneMin.csv").rename(
        columns={
            "TimeStamp": "time",
            "MeanVelocity": "ws_5",
            "MeanDirection": "wd_5",
            "MeanTemperature": "t_5",
            "MeanRH": "rh_5",
        }
    )

    boom6 = pd.read_csv(f"{data_directory}/Boom6OneMin.csv").rename(
        columns={
            "TIMESTAMP": "time",
            "MeanVelocity (m/s)": "ws_6a",
            "Mean Direction": "wd_6a",
            "MeanTemperature (C )": "t_6",
            "MeanRH (%)": "rh_6",
        }
    )

    boom7 = pd.read_csv(f"{data_directory}/Boom7OneMin.csv").rename(
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
    df = (
        boom1.merge(boom2, on="time", how="inner")
        .merge(boom6, on="time", how="inner")
        .merge(boom7, on="time", how="inner")
        .merge(boom3, on="time", how="left")
        .merge(boom4, on="time", how="left")
        .merge(boom5, on="time", how="left")
    )

    return df


def load_cid_data(data_path: str) -> pd.DataFrame:

    cid = pd.read_csv(data_path)
    cid.drop(columns=["station", "dwpc"], inplace=True)
    cid.rename(
        columns={
            "valid": "time",
            "tmpc": "t_0",
            "relh": "rh_0",
            "drct": "wd_0",
            "sped": "ws_0",
            "mslp": "p_0",
            "p01m": "precip",
        },
        inplace=True,
    )
    cid["time"] = (
        pd.to_datetime(cid["time"]).dt.tz_localize("UTC").dt.tz_convert(LOCATION.timezone)
    )
    cid = units.convert_dataframe_units(
        cid, from_units=CID_UNITS, gravity=LOCATION.g, silent=True
    )
    cid = fmt.correct_directions(
        cid
    )
    cid = cid[(cid["time"] <= pd.to_datetime('2018-08-29 00:30:00-05:00')) & (cid["time"] >= pd.to_datetime('2017-09-21 19:00:00-05:00'))].reset_index(
        drop=True
    )
    return cid


def perform_preprocessing(
    df,
    shadowing_width,
    outlier_window,
    outlier_sigma,
    resampling_window,
    turbulence_local):

    # Convert units of all columns to standard units
    df = units.convert_dataframe_units(
        df=df, from_units=SOURCE_UNITS, gravity=LOCATION.g
    )

    # Conditionally merge wind data from booms 6 and 7
    # Boom 6 (106m1, west side) is shadowed near 90 degrees (wind from east)
    # Boom 7 (106m2, east side) is shadowed near 270 degrees (wind from west)
    # Important that we do this after the conversion step, to make sure wind angles are correct
    df["ws_6"], df["wd_6"], counts = sampling.shadowing_merge(
        df=df,
        speeds=["ws_6a", "ws_6b"],
        directions=["wd_6a", "wd_6b"],
        angles=[90, 270],
        width=shadowing_width,  # Winds from within 30/2=15 degrees of tower are discarded
        drop_old=True,  # Discard the 6a and 6b columns afterwards
    )
    print(f"\tShadowing counts: {counts}")

    # Final common formatting changes:
    # ws = 0 --> wd = pd.nan; types --> float32; sorting & duplication fixes
    df = fmt.clean_formatting(df=df, type="float32")

    # Remove data according to REMOVAL_PERIODS
    if REMOVAL_PERIODS is not None:
        df, (total_dropped, partial_dropped) = qc.remove_data(df=df, periods=REMOVAL_PERIODS)
        print(f"\tManually specified removals: {total_dropped} completely, {partial_dropped} partially removed")

    # Convert time index from UTC to local time
    df = units.convert_timezone(
        df=df, source_timezone=SOURCE_TIMEZONE, target_timezone=LOCATION.timezone
    )

    # Rolling outlier removal
    len_before = df.shape[0]
    df, removals = qc.rolling_outlier_removal(
        df=df,
        window_size_minutes=outlier_window,
        sigma=outlier_sigma,
        column_types=["ws", "t", "p", "rh"],
    )
    print(f"\tOutliers removed: {removals} ({(100*removals/len_before):.4f}% of data)")

    print("\tResampling!")
    # Resampling into 10 minute intervals
    df = sampling.resample(
        df=df,
        window_size_minutes=resampling_window,
        how="mean",
        all_booms=BOOM_LIST,
        drms=True,  # do compute directional RMS
        pti=True,  # do compute pseudo-turbulence-intensity (pseudo-TI or pti) as well as max wind speed (gust estimate)
        turbulence_reference=-1 if turbulence_local else 6 # -1 indicates local
    )

    # Remove rows where there isn't enough data (not enough columns, or missing either 10m or 106m data)
    df, removed = qc.strip_missing_data(df=df, necessary=[1, 2, 6], minimum=4)
    print(f"\tRemoved {removed} rows without enough data")

    return df


def compute_values(df):
    df = compute.virtual_potential_temperatures(
        df=df, booms=[2, 6], heights=[10, 106], substitutions={"p_2": "p_1"}
    )

    df = compute.environmental_lapse_rate(
        df=df, variable="vpt", booms=[2, 6], heights=[10, 106]
    )

    df = compute.bulk_richardson_number(
        df=df, booms=[2, 6], heights=[10, 106], gravity=LOCATION.g
    )

    df = compute.classifications(
        df=df,
        terrain_classifier=TERRAIN_CLASSIFIER,
        stability_classifier=STABILITY_CLASSIFIER,
    )

    df = compute.veer(
        df=df,
        booms=[6, 4],
        colname='veer6-4',
    )  # + is clockwise turn with height (veer, expect in instability / day), - is counterclockwise (backing, expect in stability / night)

    df = compute.power_law_fits(
        df=df, booms=BOOM_LIST, heights=HEIGHT_LIST, columns=[None, "alpha"]
    )

    df, failed = compute.strip_failures(df=df, subset=["Ri_bulk", "alpha"])
    print(f"\tFailed to compute Ri_bulk and alpha for {failed} rows")

    return df.reset_index()


def save_results(df: pd.DataFrame, cid: pd.DataFrame):
    os.makedirs(SAVEDIR, exist_ok=True)
    df.to_csv(os.path.join(SAVEDIR, "output.csv"))
    df.to_parquet(os.path.join(SAVEDIR, "output.parquet"))
    cid.to_csv(os.path.join(SAVEDIR, "cid.csv"))
    cid.to_parquet(os.path.join(SAVEDIR, "cid.parquet"))


def main():
    args = parse()

    print("Loading KCC data...")
    df = load_data(args["data"])

    print("Preprocessing...")
    df = perform_preprocessing(
        df,
        shadowing_width=30,
        outlier_window=30,
        outlier_sigma=5,
        resampling_window=10,
        turbulence_local=True
    )

    print("Computing...")
    df = compute_values(df)
    print(f"Final dataset has {df.shape[0]} rows")

    print("Loading CID data...")
    cid = load_cid_data(args["cid"])

    print("Saving processed results...")
    save_results(df, cid)


if __name__ == "__main__":
    main()
