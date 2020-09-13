import pandas as pd
from sqlalchemy import create_engine, types

df = pd.read_csv('kasprowy_2020_s_d_t.csv')
print(df)

engine = create_engine('mysql+pymysql://administrator:Password123#@!@localhost/lawiny_test')
with engine.connect() as conn, conn.begin():
    df.to_sql('kasprowy2020_s_d_t', conn, if_exists='replace')


