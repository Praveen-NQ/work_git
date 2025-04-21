# 'idealpos-upload-payments'
import os
import json
import pandas as pd
from google.cloud import storage

# Set your credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/apple/.config/gcloud/application_default_credentials.json"

# Connect to GCS
client = storage.Client()
bucket = client.get_bucket('idealpos-upload-payments')
blob = bucket.blob('116/2025-04-04083701.json')

# Read and parse JSON content
content = blob.download_as_text()
data = json.loads(content)

# Flatten the nested JSON
df = pd.json_normalize(data)

# Preview all available columns to understand the structure
print("\n🔍 Available Columns:")
print(df.columns.tolist())

# Then select the right column names (based on flattened structure)
# Example if your data had nested keys under 'Transaction'
cols = [
    'Transaction.TransactionDate',
    'Transaction.TransID',
    'Transaction.TenderDescription',
    'Transaction.SalesAmount',
    'Transaction.BankingAmount'
]

# Filter only those columns that exist (safe way)
existing_cols = [col for col in cols if col in df.columns]

# Print a table preview
print("\n📋 Preview:")
print(df[existing_cols].head())
