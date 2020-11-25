import pandas as pd


LIST_CITY = ["львов+","кривой_рог+","симферополь+","и_франк+","донецк+","харьков+","днепропетровськ+","киев+","одесса+","луганськ+"]

t = 0
for j in LIST_CITY:
    data_fr = pd.DataFrame()
    for i in range(1,13):
        data_fr = data_fr.append(pd.read_excel(j+"/2012-"+str(i)+".xlsx"))
    data_fr.to_csv(str(t) + ".csv")
    t += 1
    # LIST_DF.append(data_fr)

print(pd.read_csv("1.csv"))
