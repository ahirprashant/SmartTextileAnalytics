import pandas as pd
import random

inventory = []

warehouses = [
    "Surat Warehouse",
    "Ahmedabad Warehouse",
    "Rajkot Warehouse"
]

for product_id in range(1, 501):

    stock = random.randint(50, 1000)

    reorder_level = random.randint(50, 150)

    inventory.append({
        "inventory_id": product_id,
        "product_id": product_id,
        "stock": stock,
        "reorder_level": reorder_level,
        "warehouse": random.choice(warehouses)
    })

df = pd.DataFrame(inventory)

df.to_csv("datasets/inventory.csv", index=False)

print("✅ Inventory Generated Successfully")
print(df.head())