# This script reads a JSON file from Google Cloud Storage, extracts specific fields, and converts it to a pandas DataFrame.
import os
import json
import pandas as pd
from google.cloud import storage

# Auth setup
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/apple/.config/gcloud/application_default_credentials.json"

# GCS client setup
client = storage.Client()
bucket = client.get_bucket('idealpos-upload-payments')

date_prefix = '116/2025-04-04'
# List blobs with the specified prefix
blob = bucket.list_blobs('prefix=date_prefix')

all_records = []
for blob in bucket.list_blobs():
    if blob.name.endswith('.json') and blob.name.startswith(date_prefix):
        print(f"reading file: {blob.name}")
        try:
            content = blob.download_as_text()
            data = json.loads(content)  # Parse JSON content
            records = data.get("data", [])  # Extract the nested "data" list
            all_records.extend(records)  # Append records to the list
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {blob.name}: {e}")

'''
# Read and parse JSON
content = blob.download_as_text()
data = json.loads(content)  # Parsed here

# Extract the nested "data" list
transactions = data.get("data", [])
'''
# Convert to DataFrame
df = pd.DataFrame(all_records)

# Select only required columns
required_cols = ["Venue_ID", "TransactionDate", "TransID", "TenderDescription", "SalesAmount", "BankingAmount"]
df_filtered = df[required_cols]

# Display preview
print("\n Filtered Preview:")
print(df_filtered.head())

# Save to CSV
output_file = '/Users/apple/Documents/Project/Testingsss/filtered_transactions.csv'
df_filtered.to_csv(output_file, index=False)
print(f"\nFiltered data saved to {output_file}")