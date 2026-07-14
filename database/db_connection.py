import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="smart_textile_analytics",
        user="postgres",
        password="postgres",
        port="5432"
    )

    print("✅ Database Connected Successfully!")

except Exception as e:
    print("❌ Error:", e)