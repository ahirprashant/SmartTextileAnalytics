import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="localhost",
    database="smart_textile_analytics",
    user="postgres",
    password="YOUR_PASSWORD",
    port="5432"
)

query = "SELECT * FROM sales"

df = pd.read_sql(query, conn)

print("\n========== DATA ==========")
print(df)

print("\n========== SHAPE ==========")
print(df.shape)

print("\n========== INFO ==========")
print(df.info())

print("\n========== NULL VALUES ==========")
print(df.isnull().sum())

print("\n========== DUPLICATES ==========")
print(df.duplicated().sum())

conn.close()

