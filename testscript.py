import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import ast
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import seaborn as sns
import pymysql


#%%

activities = {'paragliding', 'mountain_biking', 'snowshoeing', 'via_ferrata', 'rock_climbing', 'ice_climbing', 'snow_ice_mixed', 'skitouring', 'hiking', 'mountain_climbing'}


#%%

dates = pd.date_range(start='1/1/2015', end='1/07/2019')
dates = [el.strftime("%Y-%m-%d") for el in dates]

#%%

# d = {"date":dates, 'paragliding': [0]*len(dates), 'mountain_biking': [0]*len(dates), 'snowshoeing': [0]*len(dates), 'via_ferrata': [0]*len(dates), 'rock_climbing': [0]*len(dates), 'ice_climbing': [0]*len(dates), 'snow_ice_mixed': [0]*len(dates), 'skitouring': [0]*len(dates), 'hiking': [0]*len(dates), 'mountain_climbing': [0]*len(dates), 'paragliding_warun': [0]*len(dates), 'mountain_biking_warun': [0]*len(dates), 'snowshoeing_warun': [0]*len(dates), 'via_ferrata_warun': [0]*len(dates), 'rock_climbing_warun': [0]*len(dates), 'ice_climbing_warun': [0]*len(dates), 'snow_ice_mixed_warun': [0]*len(dates), 'skitouring_warun': [0]*len(dates), 'hiking_warun': [0]*len(dates), 'mountain_climbing_warun': [0]*len(dates)}
d = {"date":dates,'paragliding_warun': [0]*len(dates), 'mountain_biking_warun': [0]*len(dates), 'snowshoeing_warun': [0]*len(dates), 'via_ferrata_warun': [0]*len(dates), 'rock_climbing_warun': [0]*len(dates), 'ice_climbing_warun': [0]*len(dates), 'snow_ice_mixed_warun': [0]*len(dates), 'skitouring_warun': [0]*len(dates), 'hiking_warun': [0]*len(dates), 'mountain_climbing_warun': [0]*len(dates)}

df = pd.DataFrame(data=d)
df.head()

#%%

for activity in activities:

    query = "select distinct(date_start) as date, avg(condition_rating) as cnt from c2c_outings where {0} = 1 group by date_start".format(activity)
    conn = pymysql.connect("localhost", "administrator", "Password123#@!", "c2c_outings")

    df_tmp = pd.read_sql(query, con=conn)    
    conn.close()
    column_name = "{0}_warun".format(activity)
    for i in range(len(df["date"])):
        try:
            df.at[i, column_name] = df_tmp[df_tmp["date"] == df["date"][i]]["cnt"]
        except Exception:
            df.at[i, column_name] = -1 ###########BRAK PRZEJS WARUN = -1 !!!!
    print("poszlo 1")


#%%

df.head()

#%%

df["rock_climbing_warun"].plot()

#%%

plt.rcParams['figure.figsize'] = [10, 5]
sns.heatmap(df.corr(), annot=True)
plt.title("korelacja warunu")
plt.gcf().subplots_adjust(bottom=0.15)
plt.tight_layout()
plt.show()