import pandas as pd
import random

categories = {
    "Women Wear": [
        "Cotton Saree",
        "Silk Saree",
        "Designer Saree",
        "Kurti",
        "Dress Material"
    ],
    "Men Wear": [
        "Shirt Fabric",
        "Denim Fabric",
        "Cotton Shirt",
        "Formal Shirt",
        "T-Shirt"
    ],
    "Fabric": [
        "Cotton Fabric",
        "Linen Fabric",
        "Rayon Fabric",
        "Polyester Fabric",
        "Printed Fabric"
    ]
}

brands = [
    "Arvind",
    "Vimal",
    "Garden",
    "Donear",
    "Raymond",
    "Local Brand"
]

gst_rates = [5, 12, 18]

products = []

product_id = 1

while product_id <= 500:

    category = random.choice(list(categories.keys()))

    product_name = random.choice(categories[category])

    cost_price = random.randint(200, 3000)

    selling_price = cost_price + random.randint(100, 1000)

    products.append({
        "product_id": product_id,
        "product_name": product_name,
        "category": category,
        "brand": random.choice(brands),
        "fabric": product_name.split()[0],
        "cost_price": cost_price,
        "selling_price": selling_price,
        "gst": random.choice(gst_rates)
    })

    product_id += 1

df = pd.DataFrame(products)

df.to_csv("datasets/products.csv", index=False)

print("✅ 500 Products Generated Successfully")
print(df.head())