from faker import Faker
import random
import pandas as pd

fake = Faker("en_IN")

cities = [
    "Surat",
    "Ahmedabad",
    "Vadodara",
    "Rajkot",
    "Bhavnagar",
    "Anand",
    "Vapi",
    "Bharuch",
    "Jamnagar",
    "Gandhinagar"
]

customer_types = ["Retail", "Wholesale"]

customers = []

for i in range(1, 10001):
    customers.append({
    "customer_id": i,
    "customer_name": fake.name(),
    "mobile": fake.msisdn()[:10],
    "city": random.choice(cities),
    "customer_type": random.choice(customer_types),
    "join_date": fake.date_between(start_date="-3y", end_date="today"),
    "email": fake.email()
})

df = pd.DataFrame(customers)

df.to_csv("datasets/customers.csv", index=False)

print("✅ 10,000 Customers Generated Successfully")
print(df.head())