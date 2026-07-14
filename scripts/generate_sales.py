import pandas as pd
import random
from datetime import datetime, timedelta


customers = pd.read_csv("datasets/customers.csv")
products = pd.read_csv("datasets/products.csv")



payment_methods = [
    "Cash",
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking"
]

sales = []

start_date = datetime(2024, 1, 1)
end_date = datetime(2026, 12, 31)

number_of_sales = 100000


def random_date():
    days = (end_date - start_date).days
    return start_date + timedelta(days=random.randint(0, days))


for sale_id in range(1, number_of_sales + 1):

    customer = customers.sample(1).iloc[0]
    product = products.sample(1).iloc[0]

    customer_type = customer["customer_type"]

    # Wholesale customers buy more
    if customer_type == "Wholesale":
        quantity = random.randint(10, 50)
    else:
        quantity = random.randint(1, 5)

    selling_price = float(product["selling_price"])
    cost_price = float(product["cost_price"])

    discount = random.choice([0, 5, 10, 15, 20])

    gst = float(product["gst"])

    subtotal = selling_price * quantity

    discount_amount = subtotal * discount / 100

    taxable_amount = subtotal - discount_amount

    gst_amount = taxable_amount * gst / 100

    total_amount = taxable_amount + gst_amount

    profit = (selling_price - cost_price) * quantity

    sales.append({
        "sale_id": sale_id,
        "customer_id": int(customer["customer_id"]),
        "product_id": int(product["product_id"]),
        "quantity": quantity,
        "unit_price": selling_price,
        "cost_price": cost_price,
        "discount": discount,
        "gst": gst,
        "total_amount": round(total_amount, 2),
        "profit": round(profit, 2),
        "payment_method": random.choice(payment_methods),
        "sale_date": random_date().strftime("%Y-%m-%d")
    })


sales_df = pd.DataFrame(sales)



sales_df.to_csv("datasets/sales.csv", index=False)

print("=" * 50)
print("✅ Sales Dataset Generated Successfully")
print("=" * 50)

print(sales_df.head())

print("\nShape :", sales_df.shape)

print("\nColumns :")
print(sales_df.columns.tolist())

print("\nFile Saved : datasets/sales.csv")