from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import pandas as pd
import pymysql
import operator

def find_params(date, lag=2):
    dates_last_n = pd.date_range(end=date, periods=lag, freq='D')
    dates_last_n = [[el.day,el.month,el.year] for el in dates_last_n]

    importantWeatherCols = ['max_temperature', 'min_temperature', 'avg_temperature', 'percipation_sum',
                             'snow_height', 'snow_water_equivalent', 'insolation',
                            'snowfall_duration',
                            'snow_rainfall_duration', 'fog_duration', 'frost_duration', 'glaze_duration',
                            'low_snowstorm_duration',
                            'high_snowstorm_duration', 'wind_10ms_duration', 'wind_15ms_duration']

    query1 = "select * from kasprowy2019_s_d where month=12"
    query2 = "select * from kasprowy2020_s_d where month=1 or month=2 or month=3"
    conn = pymysql.connect("localhost", "administrator", "Password123#@!", "lawiny_test")
    df_weather_2019 = pd.read_sql(query1, con=conn)
    df_weather_2020 = pd.read_sql(query2, con=conn)
    conn.close()

    df_weather = [df_weather_2019, df_weather_2020]
    df_weather = pd.concat(df_weather)

    weather = []
    for i in range(lag):
        try:
            tmp_df = df_weather[(df_weather["day"] == dates_last_n[i][0]) & (df_weather["month"] == dates_last_n[i][1]) & (df_weather["year"] == dates_last_n[i][2])]
            tmp_df = tmp_df.loc[tmp_df.index[0]]
            wthr = tmp_df[importantWeatherCols].tolist()
        except Exception:
            return "KUPA"
        else:
            weather += wthr
    return weather

LAGS = 2
y = []
X = []

query = "select date, level from danger_level"
conn = pymysql.connect("localhost","administrator","Password123#@!","lawiny_test" )
df_danger_level = pd.read_sql(query, con=conn)
#print(df_danger_level)
conn.close()

for el in df_danger_level.index:
    danger = df_danger_level.loc[el]["level"]
    date = df_danger_level.loc[el]["date"]
    weather = find_params(date, lag=LAGS)
    if weather != "KUPA":
        y.append(danger)
        X.append(weather)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

#%%

clf = RandomForestClassifier(n_estimators=6000, max_depth=10, random_state=0, n_jobs=-1, criterion="entropy")
clf.fit(X, y)

#%%

y_pred = clf.predict(X_test)

#%%

confusion_matrix = confusion_matrix(y_test, y_pred)

importantWeatherCols = ['max_temperature', 'min_temperature', 'avg_temperature', 'percipation_sum',
                        'snow_height', 'snow_water_equivalent', 'insolation',
                        'snowfall_duration',
                        'snow_rainfall_duration', 'fog_duration', 'frost_duration', 'glaze_duration',
                        'low_snowstorm_duration',
                        'high_snowstorm_duration', 'wind_10ms_duration', 'wind_15ms_duration']
names = []
for no in list(range(LAGS))[::-1]:
    names+=[el+"_{0}".format(no) for el in importantWeatherCols]

tmp = list(zip(names,clf.feature_importances_))
sorted_list = sorted(tmp, key=operator.itemgetter(1), reverse=True)
dupa=0