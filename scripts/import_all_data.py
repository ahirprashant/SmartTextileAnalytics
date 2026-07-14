import pandas as pd
from sqlalchemy import create_engine

# ===== PostgreSQL Connection =====
DB_USER = "postgres"
DB_PASSWORD = "postgres"      # અહીં તમારો Password લખો
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "smart_textile_analytics"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ===== Import Function =====
def import_csv(file_path, table_name):
    print(f"Importing {table_name}...")

    df = pd.read_csv(file_path)

    df.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    print(f"✅ {table_name} Imported Successfully ({len(df)} records)")


# ===== Import All Files =====
import_csv("datasets/customers.csv", "customers")
import_csv("datasets/products.csv", "products")
import_csv("datasets/suppliers.csv", "suppliers")
import_csv("datasets/inventory.csv", "inventory")
import_csv("datasets/sales.csv", "sales")

print("\n🎉 All Data Imported Successfully")