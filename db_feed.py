import pandas as pd
from sqlalchemy import create_engine, types

df_kasprowy_2020_s_d_t = pd.read_csv('kasprowy_2020_s_d_t.csv')
df_kasprowy_2020_s_d = pd.read_csv('kasprowy_2020_s_d.csv')
df_kasprowy_2019_s_d_t = pd.read_csv('kasprowy_2019_s_d_t.csv')
df_kasprowy_2019_s_d = pd.read_csv('kasprowy_2019_s_d.csv')

engine = create_engine('mysql+pymysql://administrator:Password123#@!@localhost/lawiny_test')

with engine.connect() as conn, conn.begin():
    df_kasprowy_2020_s_d_t.to_sql('kasprowy2020_s_d_t', conn, if_exists='replace')
    df_kasprowy_2020_s_d.to_sql('kasprowy2020_s_d', conn, if_exists='replace')
    df_kasprowy_2019_s_d_t.to_sql('kasprowy2019_s_d_t', conn, if_exists='replace')
    df_kasprowy_2019_s_d.to_sql('kasprowy2019_s_d', conn, if_exists='replace')

