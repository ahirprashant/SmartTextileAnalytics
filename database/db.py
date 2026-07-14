import psycopg2

def get_connection():

    conn = psycopg2.connect(
        host="localhost",
        database="smart_textile_analytics",
        user="postgres",
        password="postgres",   # તમારો Password
        port="5432"
    )

    return conn