from collections import namedtuple

LIST_CITY = [
    "львов+",
    "кривой_рог+",
    "симферополь+",
    "и_франк+",
    "донецк+",
    "харьков+",
    "днепропетровськ+",
    "киев+",
    "одесса+",
    "луганськ+",
]
NUM_MONTHS = 12
NUM_CITIES = 10
YEAR = 2012
DEFAULT_TEMP = 18.23
DEFAULT_ENERGY_COSTS = {
    "1": 16.784,
    "2": 12.76,
    "3": 19.20,
    "4": 23.20,
    "5": 17.74,
    "6": 12.80,
}
FIGURE_SIZE = (30, 10)
SRC_PATH = "../data/src/"
CSV_PATH = "../data/cvs/"
WIND_SAMPLE_SIZE = 1500
WIND_SPEED_MULTIPLIER = 6
WIND_DIRECTION_MULTIPLIER = 360
WATER_DENSITY = 998.23
HEAT_CAPACITY = 1.163
TEMP_RANGE_START = -20
TEMP_RANGE_END = 20
TEMP_ADJUSTMENT = 30

WaterParams = namedtuple(
    "WaterParams",
    [
        "shower_duration",
        "shower_flow_rate",
        "shower_temp",
        "bath_duration",
        "bath_flow_rate",
        "bath_temp",
        "cold_water_temp",
        "hot_water_temp",
        "supply_temp",
        "efficiency",
    ],
)
