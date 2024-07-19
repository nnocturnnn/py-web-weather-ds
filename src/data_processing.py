import os
import pandas as pd
from constants import (
    LIST_CITY,
    NUM_MONTHS,
    SRC_PATH,
    CSV_PATH,
    YEAR,
    NUM_CITIES,
    WaterParams,
)


def read_monthly_data(city, month):
    file_path = os.path.join(city, f"2012-{month}.xlsx")
    try:
        monthly_data = pd.read_excel(file_path)
        monthly_data["Mon"] = month
        return monthly_data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return pd.DataFrame()


def process_city_data(city):
    city_data_frames = []
    for month in range(1, NUM_MONTHS + 1):
        monthly_data = read_monthly_data(city, month)
        city_data_frames.append(monthly_data)
    data_frame = pd.concat(city_data_frames, ignore_index=True)
    return data_frame


def create_dataframe_from_files():
    for index, city in enumerate(SRC_PATH + LIST_CITY):
        data_frame = process_city_data(city)
        csv_path = os.path.join(CSV_PATH, f"{index}.csv")
        try:
            data_frame.to_csv(csv_path, index=False)
        except Exception as e:
            print(f"Error writing {csv_path}: {e}")


def clean_dataframes():
    for index in range(NUM_CITIES):
        csv_path = os.path.join(CSV_PATH, f"{index}.csv")
        try:
            df = pd.read_csv(csv_path)
        except FileNotFoundError:
            print(f"File not found: {csv_path}")
            continue
        except Exception as e:
            print(f"Error reading {csv_path}: {e}")
            continue

        df = df.fillna("0")
        df["Число месяца"] = df["Число месяца"].astype(int)
        df["Mon"] = df["Mon"].astype(int)

        df["UTC"] = (
            f"{YEAR}."
            + df["Mon"].astype(str)
            + "."
            + df["Число месяца"].astype(str)
            + "."
            + df["UTC"]
        )
        df["UTC"] = pd.to_datetime(
            df["UTC"], format="%Y.%m.%d.%H:%M:%S", errors="coerce"
        )

        df.drop(columns=["Число месяца", "Mon", "U"], inplace=True)

        try:
            df.to_csv(csv_path, index=False)
        except Exception as e:
            print(f"Error writing {csv_path}: {e}")


def parse_water_params(param_str):
    params_list = list(map(int, param_str.split("/")))
    return WaterParams._make(params_list)
