import pandas as pd
import numpy as np
from windrose import WindroseAxes
from constants import (
    FIGURE_SIZE,
    DEFAULT_ENERGY_COSTS,
    DEFAULT_TEMP,
    LIST_CITY,
    YEAR,
    WIND_SAMPLE_SIZE,
    WIND_SPEED_MULTIPLIER,
    WIND_DIRECTION_MULTIPLIER,
    TEMP_RANGE_START,
    TEMP_RANGE_END,
    TEMP_ADJUSTMENT,
)
from data_processing import parse_water_params
from calculations import (
    shower_heat_quantity,
    bath_heat_quantity,
    temp_adjusted_heat_quantity,
    hot_water_heat_quantity,
    hot_water_energy,
    compute_costs,
)


class PlotFactory:
    @staticmethod
    def create_plotter(params):
        plotters = {
            "T_plot": lambda df, params: plot_t_plot(df, params),
            "T_val_plot": lambda df, params: plot_t_val_plot(df),
            "sun_izo": lambda df, params: plot_sun_izo(df, params),
            "val_wind": lambda df, params: plot_val_wind(df),
            "val_sun_izo": lambda df, params: plot_val_sun_izo(df),
            "Wind": lambda df, params: plot_wind(),
        }
        
        if params["exer"] in plotters:
            return plotters[params["exer"]]
        elif params["exer_2"] in ["2_7", "2_4"]:
            return lambda df, params: plot_cost_comparison(params, df)
        return None
    

def get_plot(params):
    city = params["city"]
    city_index = LIST_CITY.index(city + "+")
    data_frame = pd.read_csv(f"{city_index}.csv", index_col=0)
    data_frame["UTC"] = pd.to_datetime(data_frame["UTC"])
    start_date, end_date = params["date"].split("-")
    start_date_formatted = f"{YEAR}-{start_date[3:5]}-{start_date[:2]}"
    end_date_formatted = f"{YEAR}-{end_date[3:5]}-{end_date[:2]}"
    filtered_data = data_frame[
        (data_frame["UTC"] >= start_date_formatted)
        & (data_frame["UTC"] <= end_date_formatted)
    ]
    plot_object = plot_data(filtered_data, params)
    figure = plot_object.get_figure()
    return figure


def plot_data(df, params):
    plotter = PlotFactory.create_plotter(params)
    if plotter is not None:
        return plotter(df, params)
    return None


def plot_t_plot(df, params):
    df.drop(columns=["FF", "N", "PPP", "hhh", "Unnamed: 0.1"], inplace=True)
    plt_obj = df.plot(figsize=FIGURE_SIZE)
    plt_obj.set_ylabel("Sun Izo")
    plt_obj.set_xlabel("Date")
    plt_obj.set_title(params["city"])
    return plt_obj


def plot_t_val_plot(df):
    df.drop(columns=["FF", "N", "PPP", "hhh", "Unnamed: 0.1"], inplace=True)
    temp_counts = df["T"].value_counts().sort_index()
    plt_obj = temp_counts.plot.bar(figsize=FIGURE_SIZE)
    return plt_obj


def plot_sun_izo(df, params):
    df.drop(columns=["FF", "N", "PPP", "T", "Unnamed: 0.1"], inplace=True)
    plt_obj = df.plot(figsize=FIGURE_SIZE)
    plt_obj.set_ylabel("Temperature")
    plt_obj.set_xlabel("Date")
    plt_obj.set_title(params["city"])
    return plt_obj


def plot_val_wind(df):
    df.drop(columns=["T", "N", "PPP", "hhh", "Unnamed: 0.1"], inplace=True)
    wind_counts = df["FF"].value_counts().sort_index()
    plt_obj = wind_counts.plot.bar(figsize=FIGURE_SIZE)
    plt_obj.set_ylabel("Wind")
    plt_obj.set_xlabel("Num")
    plt_obj.set_title("Wind")
    return plt_obj


def plot_val_sun_izo(df):
    df.drop(columns=["FF", "N", "PPP", "T", "Unnamed: 0.1"], inplace=True)
    sun_counts = df["hhh"].value_counts().sort_index()
    plt_obj = sun_counts.plot.bar(figsize=FIGURE_SIZE)
    return plt_obj


def plot_wind():
    ws = np.random.random(WIND_SAMPLE_SIZE) * WIND_SPEED_MULTIPLIER
    wd = np.random.random(WIND_SAMPLE_SIZE) * WIND_DIRECTION_MULTIPLIER
    ax = WindroseAxes.from_ax()
    ax.bar(wd, ws, normed=True, opening=0.8, edgecolor="white")
    ax.set_legend()
    plt_obj = ax.get_figure()
    return plt_obj


def plot_cost_bar_chart(cost_list):
    cost_df = pd.DataFrame(
        cost_list, index=DEFAULT_ENERGY_COSTS.keys(), columns=["Cost"]
    )
    plot_object = cost_df.plot.bar(figsize=FIGURE_SIZE)
    return plot_object


def plot_temperature_graph(hot_water_energy):
    temp_graph = {
        i: i * hot_water_energy for i in range(TEMP_RANGE_START, TEMP_RANGE_END)
    }
    temp_df = pd.DataFrame.from_dict(
        temp_graph, orient="index", columns=["Temperature"]
    )
    plot_object = temp_df.plot(figsize=FIGURE_SIZE, marker=".", markersize=10)
    plot_object.grid()
    return plot_object


def plot_cost_comparison(params, df):
    adjusted_temp_count = (df["T"] == params["sli"] - TEMP_ADJUSTMENT).sum()
    base_cost = adjusted_temp_count * DEFAULT_TEMP
    water_params = parse_water_params(params["s_s"] + "/" + params["s_s_s"])

    shower_heat_qty = shower_heat_quantity(water_params)
    bath_heat_qty = bath_heat_quantity(water_params)
    shower_temp_qty = temp_adjusted_heat_quantity(
        shower_heat_qty,
        water_params.shower_temp,
        water_params.cold_water_temp,
        water_params.hot_water_temp,
    )
    bath_temp_qty = temp_adjusted_heat_quantity(
        bath_heat_qty,
        water_params.bath_temp,
        water_params.cold_water_temp,
        water_params.hot_water_temp,
    )
    hot_water_heat_qty = hot_water_heat_quantity(shower_temp_qty, bath_temp_qty)
    hot_water_energy_value = hot_water_energy(hot_water_heat_qty, water_params)

    if params["exer_2"] == "2_7":
        efficiency_factor = int(params["s_six_t"])
        cost_list = compute_costs(base_cost, hot_water_energy_value, efficiency_factor)
        plot_object = plot_cost_bar_chart(cost_list)
    elif params["exer_2"] == "2_4":
        plot_object = plot_temperature_graph(hot_water_energy_value)
    return plot_object
