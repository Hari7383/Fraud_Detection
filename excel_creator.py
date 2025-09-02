import pandas as pd
import random
from faker import Faker
import numpy as np
import os

fake = Faker()

# Set seed for reproducibility
Faker.seed(0)
random.seed(0)
np.random.seed(0)

# Generate 1000 rows
n_rows = 1000
data = []

transaction_types = ['purchase', 'refund']
device_ids = [f'DEV{str(i).zfill(4)}' for i in range(1, 201)]  # 200 unique devices
user_ids = [f'U{str(i).zfill(4)}' for i in range(1, 501)]      # 500 unique users

for i in range(n_rows):
    transaction_id = f'TXN{str(100000 + i)}'
    user_id = random.choice(user_ids)
    ip_address = fake.ipv4_public()
    device_id = random.choice(device_ids)
    transaction_type = random.choices(transaction_types, weights=[0.85, 0.15])[0]  # 15% refunds
    transaction_time = fake.date_time_between(start_date='-30d', end_date='now')
    transaction_amount = round(random.uniform(10, 500), 2)
    
    data.append([
        transaction_id,
        user_id,
        ip_address,
        device_id,
        transaction_type,
        transaction_time,
        transaction_amount
    ])

# Create DataFrame
df = pd.DataFrame(data, columns=[
    'transaction_id', 'user_id', 'ip_address', 'device_id',
    'transaction_type', 'transaction_time', 'transaction_amount'
])

# Print first 5 rows to verify data generation
print("Sample data (first 5 rows):")
print(df.head())

# Save to Excel
filename = "fraud_detection_sample_data.xlsx"
df.to_excel(filename, index=False)

# Check if file is created
if os.path.exists(filename):
    print(f"\nExcel file '{filename}' created successfully in the directory:\n{os.getcwd()}")
else:
    print("\nFailed to create the Excel file.")   