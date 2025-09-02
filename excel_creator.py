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

# Define fraud classification logic (example):
def classify_fraud(row):
    if row['transaction_type'] == 'refund' and row['transaction_amount'] > 300:
        return 'fraud'
    elif row['transaction_type'] == 'purchase' and row['transaction_amount'] > 450:
        return 'fraud'
    else:
        return 'not fraud'

classified_df = df[['transaction_id']].copy()
classified_df['fraud_status'] = df.apply(classify_fraud, axis=1)

# Calculate starting column for classified_df: 
# main df has 7 columns (0-indexed columns 0 to 6), so startcol=7 to write classified_df next to it
start_col = len(df.columns) + 1  # adding 1 column as a gap

filename = "fraud_detection_sample_data.xlsx"

with pd.ExcelWriter(filename, engine='openpyxl') as writer:
    # Write main data starting at cell A1 (row=0, col=0)
    df.to_excel(writer, sheet_name='Transactions', index=False)
    
    # Write classified_df starting at first row, after the last column of main data (+1 for gap)
    classified_df.to_excel(writer, sheet_name='Transactions', index=False, startcol=start_col)

# Confirm file creation
if os.path.exists(filename):
    print(f"\nExcel file '{filename}' created successfully in:\n{os.getcwd()}")
else:
    print("\nFailed to create the Excel file.")
