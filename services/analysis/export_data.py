from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(
    "postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/smart_textile_analytics"
)

df = pd.read_sql("SELECT * FROM sales", engine)

df.to_csv("datasets/clean_sales.csv", index=False)

print("Clean Data Exported Successfully")