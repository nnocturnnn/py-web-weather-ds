import pandas as pd
from spyre import server
import json
import datetime
import matplotlib.pyplot as plt

# t = 0
# for j in LIST_CITY:              # create df from files
#     data_fr = pd.DataFrame()
#     for i in range(1,13):
#         data_fr = data_fr.append(pd.read_excel(j+"/2012-"+str(i)+".xlsx"))
#         if i == 1:
#             data_fr["Mon"] = 1
#         else:
#             data_fr["Mon"] = data_fr["Mon"].fillna(i)
#     data_fr.to_csv(str(t) + ".csv")
#     t += 1
    # LIST_DF.append(data_fr)

# for i in range(3,10):          # fix date and clean db
#     df = pd.read_csv(str(i) + ".csv")
#     df = df.fillna("0")
#     df['Число месяца'] = df['Число месяца'].astype(int)
#     df['Mon'] = df['Mon'].astype(int)
#     df['UTC'] = df['Число месяца'].astype(str) + "." + df['UTC']
#     df['UTC'] = df['Mon'].astype(str) + "." + df['UTC']
#     del df['Число месяца']
#     del df['Mon']
#     del df['U']
#     df['UTC'] = pd.to_datetime(df['UTC'],format='%m.%d.%H:%M:%S', errors='coerce')
#     df.to_csv(str(i) + ".csv")


class StockExample(server.App):
    title = "Weather"

    inputs = [{     "type":'dropdown',
                    "label": 'City',
                    "options" : [ {"label": "львов", "value":"львов"},
                                  {"label": "кривой_рог", "value":"кривой_рог"},
                                  {"label": "симферополь", "value":"симферополь"},
                                  {"label": "и_франк", "value":"и_франк"},
                                  {"label": "донецк", "value":"донецк"},
                                  {"label": "харьков", "value":"харьков"},
                                  {"label": "днепропетровськ", "value":"днепропетровськ"},
                                  {"label": "киев", "value":"киев"},
                                  {"label": "одесса", "value":"одесса"},
                                  {"label": "луганськ", "value":"луганськ"},],
                    "key": 'city',
                    "action_id": "update_data"},
                    {     "type":'dropdown',
                    "label": 'Exercise',
                    "options" : [ {"label": "T_plot", "value":"T_plot"},
                                  {"label": "T_val_plot", "value":"T_val_plot"},
                                  {"label": "Wind", "value":"Wind"},
                                  {"label": "val_wind", "value":"val_wind"},
                                  {"label": "sun_izo", "value":"sun_izo"},
                                  {"label": "val_sun_izo", "value":"val_sun_izo"},],
                    "key": 'exer',
                    "action_id": "update_data"}]

    controls = [{    "type" : "hidden",
                    "id" : "update_data"}]

    tabs = ["T_plot"]

    outputs = [{ "type" : "plot",
                    "id" : "plot",
                    "control_id" : "update_data",
                    "tab" : "T_plot"},

                { "type" : "plot_4",
                    "id" : "plot_4",
                    "control_id" : "update_data",
                    "tab" : "T_val_plot",},

                { "type" : "plot",
                    "id" : "plo2",
                    "control_id" : "update_data",
                    "tab" : "Wind"},

                { "type" : "plot",
                    "id" : "plot3",
                    "control_id" : "update_data",
                    "tab" : "val_Wind"},

                { "type" : "plot",
                    "id" : "plot4",
                    "control_id" : "update_data",
                    "tab" : "sun_izo"},]

    def getPlot(self, params):
        LIST_CITY = ["львов+","кривой_рог+","симферополь+","и_франк+","донецк+","харьков+","днепропетровськ+","киев+","одесса+","луганськ+"]
        citys = params["city"]
        index = LIST_CITY.index(citys + "+")
        df = pd.read_csv(str(index) + ".csv",index_col=0)
        df = df.set_index(df['UTC'])
        if params["exer"] == "T_plot":
            del df["FF"]
            del df["N"]
            del df["PPP"]
            del df["hhh"]
            del df["Unnamed: 0.1"]
            plt_obj = df.plot(figsize=(25,5))
            plt_obj.set_ylabel("Sun Izo")
            plt_obj.set_xlabel("Date")
            plt_obj.set_title(citys)
        elif params["exer"] == "T_val_plot":
            del df["FF"]
            del df["N"]
            del df["PPP"]
            del df["hhh"]
            del df["Unnamed: 0.1"]
            dict_val = {}
            for i in range(-30,35,1):
                q = (df['T'] == i).sum()
                dict_val.update({i : q})
            dfc = pd.DataFrame.from_dict(dict_val, orient = 'index')
            plt_obj = dfc.plot.bar(figsize=(25,5))
        elif params["exer"] == "sun_izo":
            del df["FF"]
            del df["N"]
            del df["PPP"]
            del df["T"]
            del df["Unnamed: 0.1"]
            plt_obj = df.plot(figsize=(25,5))
            plt_obj.set_ylabel("Temperature")
            plt_obj.set_xlabel("Date")
            plt_obj.set_title(citys)
        elif params["exer"] == "val_wind":
            del df["T"]
            del df["N"]
            del df["PPP"]
            del df["hhh"]
            del df["Unnamed: 0.1"]
            dict_val = {}
            for i in range(0,15,1):
                q = (df['FF'] == i).sum()
                dict_val.update({i : q})
            dfc = pd.DataFrame.from_dict(dict_val, orient = 'index')
            plt_obj = dfc.plot.bar(figsize=(25,5))
            plt_obj.set_ylabel("Wind")
            plt_obj.set_xlabel("Num")
            plt_obj.set_title(citys)
        fig = plt_obj.get_figure()
        return fig

app = StockExample()
app.launch(port=9093)