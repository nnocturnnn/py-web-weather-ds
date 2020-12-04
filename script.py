import pandas as pd
from windrose import WindroseAxes
from spyre import server
import json
import datetime
import numpy as np
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
                    "label": 'Exercise1',
                    "options" : [ {"label": "T_plot", "value":"T_plot"},
                                  {"label": "T_val_plot", "value":"T_val_plot"},
                                  {"label": "Wind", "value":"Wind"},
                                  {"label": "val_wind", "value":"val_wind"},
                                  {"label": "sun_izo", "value":"sun_izo"},
                                  {"label": "val_sun_izo", "value":"val_sun_izo"},],
                    "key": 'exer',
                    "action_id": "update_data"},
                    {     "type":'dropdown',
                    "label": 'Exercise1',
                    "options" : [ {"label": "2_1", "value":"2_1"},
                                  {"label": "2_2", "value":"2_2"},
                                  {"label": "2_3", "value":"2_3"},
                                  {"label": "2_4", "value":"2_4"},
                                  {"label": "2_5", "value":"2_5"},
                                  {"label": "2_6", "value":"2_6"},
                                  {"label": "2_7", "value":"2_7"},
                                  {"label": "2_8", "value":"2_8"},],
                    "key": 'exer_2',
                    "action_id": "update_data"},
                    {
                        "type":'text',
                        "label": '2.1 Вт/м2',
                        "value" : '12',
                        "key": 's_one',
                        "action_id" : "refresh",
                    },
                    {
                        "type":'text',
                        "label": '2.1 S',
                        "value" : '3',
                        "key": 's_one_s',
                        "action_id" : "refresh",
                    },
                    {
                        "type":'text',
                        "label": '2.2: Nд/Qд/Тд/Nв/Qв/Тв',
                        "value" : '3/2/3/1/2/1',
                        "key": 's_s',
                        "action_id" : "refresh",
                    },
                    {
                        "type":'text',
                        "label": '2.2: T.вх/T.вих/Т.бака/t.нагр',
                        "value" : '3/2/2/3',
                        "key": 's_s_s',
                        "action_id" : "refresh",
                    },
                    {
                        "type":'text',
                        "label": '2.3: T.вх/T.вих/Т.бака/t.нагр',
                        "value" : '3/2/2/3',
                        "key": 's_t',
                        "action_id" : "refresh",
                    },]

    controls = [{    "type" : "hidden",
                    "id" : "update_data"}]

    tabs = ["Plot","Answer"]

    outputs = [{ "type" : "plot",
                    "id" : "plot",
                    "control_id" : "update_data",
                    "tab" : "Plot"},
                { "type" : "html",
                    "id" : "simphtml",
                    "control_id" : "update_data",
                    "tab" : "Answer",
                    "on_page_load" : True },]

    def getHTML(self, params):
        if params["exer_2"] == "2_1":
            res = int(params["s_one"]) * int(params["s_one_s"])
            return f"<a>Result : {res}</a> "
        elif params["exer_2"] == "2_2":
            List_str = params["s_s"] + "/" + params["s_s_s"]
            List_arg = List_str.split('/')
            List_arg = list(map(int, List_arg))
            print(List_arg)
            Q_d = List_arg[0] * List_arg[1]
            Q_v = List_arg[3] * List_arg[4]
            Q_td = Q_d*((List_arg[2] - List_arg[6]) / (List_arg[7] - List_arg[6]))
            Q_tv = Q_v*((List_arg[5] - List_arg[6]) / (List_arg[7] - List_arg[6]))
            Q_tgv = ((Q_td - Q_tv) / 998.23)
            W_tgv = 1.163 * Q_tgv * (List_arg[8] - List_arg[6])
            print(W_tgv,List_arg[9])
            P_gvp = W_tgv / List_arg[9]
            return f"Q душ  = {Q_d}<br>Q ванн  = {Q_v}<br>Qt душ = {Q_td}<br>Qt ванн = {Q_tv}<br>Qt г.води = {Q_tgv}<br>W г.води = {W_tgv}<br>P ГВП = {P_gvp}"
        # elif params["exer_2"] == "2_3":

        # elif params["exer_2"] == "2_4":
        # elif params["exer_2"] == "2_5":
        # elif params["exer_2"] == "2_6":
        # elif params["exer_2"] == "2_7":
        # elif params["exer_2"] == "2_8":
        return "<a>Error</a>"
    
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
            plt_obj = df.plot(figsize=(30,10))
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
            plt_obj = dfc.plot.bar(figsize=(30,10))
        elif params["exer"] == "sun_izo":
            del df["FF"]
            del df["N"]
            del df["PPP"]
            del df["T"]
            del df["Unnamed: 0.1"]
            plt_obj = df.plot(figsize=(30,10))
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
            plt_obj = dfc.plot.bar(figsize=(30,10))
            plt_obj.set_ylabel("Wind")
            plt_obj.set_xlabel("Num")
            plt_obj.set_title(citys)
        elif params["exer"] == "val_sun_izo":
            arr = df["hhh"].unique()
            del df["FF"]
            del df["N"]
            del df["PPP"]
            del df["T"]
            del df["Unnamed: 0.1"]
            dict_val = {}
            for i in arr:
                if i == 0:
                    continue
                else:
                    q = (df['hhh'] == i).sum()
                    dict_val.update({i : q})
            dfc = pd.DataFrame.from_dict(dict_val, orient = 'index')
            plt_obj = dfc.plot.bar(figsize=(30,10))
        elif params["exer"] == "Wind":
            ws_df = df["dd"].to_numpy()
            wd_df = df["FF"].to_numpy()
            ws = np.random.random(1500) * 6
            wd = np.random.random(1500) * 360
            ax = WindroseAxes.from_ax()
            ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white')
            ax.set_legend()
            fig = ax.get_figure()
            return fig
        fig = plt_obj.get_figure()
        return fig

    def getCustomCSS(self):
        return "body {background:grey;}"

app = StockExample()
app.launch(port=9093)