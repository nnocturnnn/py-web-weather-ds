import pandas as pd
from spyre.server import App
from constants import LIST_CITY
from data_processing import create_dataframe_from_files, clean_dataframes
from calculations import (
    building_thermal_characteristics,
    hot_water_parameters,
    thermal_loss_power,
    energy_cost,
    cost_comparison,
)
from plotting import get_plot


class WeatherApp(App):
    title = "Weather"

    inputs = [
        {
            "type": "dropdown",
            "label": "City",
            "options": [
                {"label": city.strip("+"), "value": city.strip("+")}
                for city in LIST_CITY
            ],
            "key": "city",
            "action_id": "update_data",
        },
        {
            "type": "text",
            "label": "Date: ",
            "value": "20.05-26.09",
            "key": "date",
            "action_id": "refresh",
        },
        {
            "type": "dropdown",
            "label": "Exercise1",
            "options": [
                {"label": "-", "value": "-"},
                {"label": "T_plot", "value": "T_plot"},
                {"label": "T_val_plot", "value": "T_val_plot"},
                {"label": "Wind", "value": "Wind"},
                {"label": "val_wind", "value": "val_wind"},
                {"label": "sun_izo", "value": "sun_izo"},
                {"label": "val_sun_izo", "value": "val_sun_izo"},
            ],
            "key": "exer",
            "action_id": "update_data",
        },
        {
            "type": "dropdown",
            "label": "Exercise2",
            "options": [{"label": f"2_{i}", "value": f"2_{i}"} for i in range(1, 8)],
            "key": "exer_2",
            "action_id": "update_data",
        },
        {
            "type": "text",
            "label": "2.1 Вт/м2",
            "value": "12",
            "key": "s_one",
            "action_id": "refresh",
        },
        {
            "type": "text",
            "label": "2.1 S",
            "value": "3",
            "key": "s_one_s",
            "action_id": "refresh",
        },
        {
            "type": "text",
            "label": "2.2: Nд/Qд/Тд/Nв/Qв/Тв",
            "value": "3/2/3/1/2/1",
            "key": "s_s",
            "action_id": "refresh",
        },
        {
            "type": "text",
            "label": "2.2: T.вх/T.вих/Т.бака/t.нагр",
            "value": "3/2/2/3",
            "key": "s_s_s",
            "action_id": "refresh",
        },
        {
            "type": "text",
            "label": "2.3: T.роз/Q.тепла/S.буд",
            "value": "3/2/2",
            "key": "s_t",
            "action_id": "refresh",
        },
        {
            "type": "slider",
            "label": "2.5: T",
            "value": "10",
            "min": -30,
            "max": 30,
            "key": "sli",
            "action_id": "refresh",
        },
        {
            "type": "dropdown",
            "label": "2.6",
            "options": [
                {"label": desc, "value": str(i + 1)}
                for i, desc in enumerate(
                    [
                        "теплозабезпечення від централізованої мережі;",
                        "автономного теплозабезпечення від газового котла;",
                        "автономного теплозабезпечення від вугільного котла;",
                        "автономного теплозабезпечення від дров’яного котла;",
                        "автономного теплозабезпечення від котла, що працює на деревних пелетах;",
                        "автономного теплозабезпечення від електричного котла.",
                    ]
                )
            ],
            "key": "s_six",
            "action_id": "update_data",
        },
        {
            "type": "text",
            "label": "2.6: N топл",
            "value": "302",
            "key": "s_six_t",
            "action_id": "refresh",
        },
    ]

    controls = [{"type": "hidden", "id": "update_data"}]
    tabs = ["Plot", "Answer"]
    outputs = [
        {"type": "plot", "id": "plot", "control_id": "update_data", "tab": "Plot"},
        {
            "type": "html",
            "id": "simphtml",
            "control_id": "update_data",
            "tab": "Answer",
            "on_page_load": True,
        },
    ]

    def getHTML(self, params):
        result = self.calculate_result(params)
        return result

    def calculate_result(self, params):
        if params["exer_2"] == "2_1":
            return building_thermal_characteristics(params)
        elif params["exer_2"] == "2_2":
            return hot_water_parameters(params)
        elif params["exer_2"] == "2_3":
            return thermal_loss_power(params)
        elif params["exer_2"] == "2_4":
            return "<a>Not implemented</a>"
        elif params["exer_2"] == "2_5":
            return energy_cost(params)
        elif params["exer_2"] in ["2_6", "2_7"]:
            return cost_comparison(params)
        return "<a>Error</a>"

    def get_plot(self, params):
        return get_plot(params)

    def getCustomCSS(self):
        return " .tab-content {background:#E2E2E2;}\
              body {background:linear-gradient(90deg, rgba(0,0,0,1) 0%,\
              rgba(255,255,255,1) 100%)}"


if __name__ == "__main__":
    create_dataframe_from_files()
    clean_dataframes()
    app = WeatherApp()
    app.launch(port=9093)
