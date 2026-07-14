import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="localhost",
    database="smart_textile_analytics",
    user="postgres",
    password="YOUR_PASSWORD",
    port="5432"
)

query = "SELECT * FROM sales;"

df = pd.read_sql(query, conn)

print(df)

conn.close()