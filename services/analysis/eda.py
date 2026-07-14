import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="localhost",
    database="smart_textile_analytics",
    user="postgres",
    password="YOUR_PASSWORD",
    port="5432"
)

df = pd.read_sql("SELECT * FROM sales", conn)

print("\n========== SUMMARY ==========")
print(df.describe())

print("\n========== TOTAL SALES ==========")
print(df["total_amount"].sum())

print("\n========== AVERAGE SALES ==========")
print(df["total_amount"].mean())

print("\n========== MAX SALE ==========")
print(df["total_amount"].max())

print("\n========== MIN SALE ==========")
print(df["total_amount"].min())

conn.close()