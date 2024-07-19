from constants import (
    DEFAULT_TEMP,
    DEFAULT_ENERGY_COSTS,
    LIST_CITY,
    WATER_DENSITY,
    HEAT_CAPACITY,
    TEMP_ADJUSTMENT,
)
import pandas as pd
from data_processing import parse_water_params
from misc import generate_description


def building_thermal_characteristics(params):
    specific_heat_loss = int(params["specific_heat_loss"])
    total_area = int(params["total_area"])
    total_heat_loss = specific_heat_loss * total_area
    return (
        f"<font style='text-align: center; size=20' face='Arial'>"
        f"Теплотехнічні характеристики будівлі:<br>"
        f"Питомі тепловтрати: {specific_heat_loss}<br>"
        f"Загальна площа: {total_area}<br>"
        f"Результат: {total_heat_loss}</font>"
    )


def hot_water_parameters(params):
    water_params = parse_water_params(params["water_params"])
    shower_heat = shower_heat_quantity(water_params)
    bath_heat = bath_heat_quantity(water_params)
    shower_temp_heat_adjusted = temp_adjusted_heat_quantity(
        shower_heat,
        water_params.shower_temp,
        water_params.cold_water_temp,
        water_params.hot_water_temp,
    )
    bath_temp_heat_adjusted = temp_adjusted_heat_quantity(
        bath_heat,
        water_params.bath_temp,
        water_params.cold_water_temp,
        water_params.hot_water_temp,
    )
    hot_water_heat = hot_water_heat_quantity(
        shower_temp_heat_adjusted, bath_temp_heat_adjusted
    )
    hot_water_energy_value = hot_water_energy(hot_water_heat, water_params)
    hot_water_system_power = hot_water_energy_value / water_params.efficiency
    return (
        f"<font style='text-align: center; size=20' face='Arial'>"
        f"Q душ: {shower_heat}<br>"
        f"Q ванн: {bath_heat}<br>"
        f"Qt душ: {shower_temp_heat_adjusted}<br>"
        f"Qt ванн: {bath_temp_heat_adjusted}<br>"
        f"Qt г.води: {hot_water_heat}<br>"
        f"W г.води: {hot_water_energy_value}<br>"
        f"P ГВП: {hot_water_system_power}</font>"
    )


def thermal_loss_power(params):
    parameters = list(map(int, params["thermal_loss_params"].split("/")))
    thermal_loss_power = parameters[0] * parameters[1] * parameters[2]
    return (
        f"<font style='text-align: center; size=20' face='Arial'>"
        f"Потужність тепловтрат: {thermal_loss_power}</font>"
    )


def energy_cost(params):
    city = params["city"]
    city_index = LIST_CITY.index(city + "+")
    data_frame = pd.read_csv(f"{city_index}.csv", index_col=0)
    temperature_count = (data_frame["T"] == params["sli"]).sum()
    energy_cost = temperature_count * DEFAULT_TEMP
    return (
        f"<font style='text-align: center; size=20' face='Arial'>"
        f"Витрати енергії на опалення: {energy_cost}</font>"
    )


def cost_comparison(params):
    city_index = LIST_CITY.index(params["city"] + "+")
    data_frame = pd.read_csv(f"{city_index}.csv", index_col=0)

    base_cost = calc_base_cost(data_frame, params["sli"])
    water_params = parse_water_params(params["s_s"] + "/" + params["s_s_s"])
    shower_heat = shower_heat_quantity(water_params)
    bath_heat = bath_heat_quantity(water_params)
    shower_temp_heat = temp_adjusted_heat_quantity(
        shower_heat,
        water_params.shower_temp,
        water_params.cold_water_temp,
        water_params.hot_water_temp,
    )
    bath_temp_heat = temp_adjusted_heat_quantity(
        bath_heat,
        water_params.bath_temp,
        water_params.cold_water_temp,
        water_params.hot_water_temp,
    )
    hot_water_heat = hot_water_heat_quantity(shower_temp_heat, bath_temp_heat)
    hot_water_energy_value = hot_water_energy(hot_water_heat, water_params)

    efficiency_factor = int(params["s_six_t"])
    energy_key = params["s_six"]
    specific_energy_cost = DEFAULT_ENERGY_COSTS[energy_key]

    total_cost = (
        base_cost * hot_water_energy_value * efficiency_factor * specific_energy_cost
    )

    if params["exer_2"] == "2_6":
        description = generate_description(energy_key)
        return (
            f"<font style='text-align: center; size=20' face='Arial'>"
            f"За відомими обсягами споживання розрахувати вартість опалення та ГВП будівлі для умов: {description} = {total_cost}"
            f"</font>"
        )

    return "<a>Error</a>"


def shower_heat_quantity(water_params):
    return water_params.shower_duration * water_params.shower_flow_rate


def bath_heat_quantity(water_params):
    return water_params.bath_duration * water_params.bath_flow_rate


def temp_adjusted_heat_quantity(heat_quantity, temp, cold_temp, hot_temp):
    return heat_quantity * (temp - cold_temp) / (hot_temp - cold_temp)


def hot_water_heat_quantity(shower_temp_quantity, bath_temp_quantity):
    return (shower_temp_quantity - bath_temp_quantity) / WATER_DENSITY


def hot_water_energy(hot_water_heat_quantity, water_params):
    return (
        HEAT_CAPACITY
        * hot_water_heat_quantity
        * (water_params.supply_temp - water_params.cold_water_temp)
    )


def compute_costs(base_cost, hot_water_energy, efficiency_factor):
    return [
        base_cost * hot_water_energy * efficiency_factor * cost
        for cost in DEFAULT_ENERGY_COSTS.values()
    ]


def calc_base_cost(data_frame, sli):
    adjusted_temp_count = (data_frame["T"] == sli - TEMP_ADJUSTMENT).sum()
    return adjusted_temp_count * DEFAULT_TEMP
