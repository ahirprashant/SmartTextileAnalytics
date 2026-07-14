from faker import Faker
import pandas as pd
import random

fake = Faker("en_IN")

cities = [
    "Surat",
    "Ahmedabad",
    "Rajkot",
    "Vadodara",
    "Bhavnagar",
    "Vapi",
    "Bharuch",
    "Anand"
]

ratings = [3, 4, 5]

suppliers = []

for i in range(1, 101):

    suppliers.append({
        "supplier_id": i,
        "supplier_name": fake.company(),
        "city": random.choice(cities),
        "contact": fake.msisdn()[:10],
        "email": fake.company_email(),
        "rating": random.choice(ratings)
    })

df = pd.DataFrame(suppliers)

df.to_csv("datasets/suppliers.csv", index=False)

print("✅ 100 Suppliers Generated Successfully")
print(df.head())