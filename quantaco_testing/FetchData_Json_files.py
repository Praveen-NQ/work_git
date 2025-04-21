import os
import json
import pandas as pd
from google.cloud import storage

# Auth setup
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/apple/.config/gcloud/application_default_credentials.json"

# GCS client setup
client = storage.Client()
bucket = client.get_bucket('idealpos-upload-payments')

# Prefix to filter files (adjust if needed)
date_prefix = '116/2025-04-05'  # Adjust date here
blobs = bucket.list_blobs(prefix=date_prefix)

# List to store all records
all_records = []

# Loop through each file
for blob in blobs:
    if blob.name.endswith('.json') and blob.name.startswith(date_prefix):
        print(f"📂 Processing file: {blob.name}")

        try:
            content = blob.download_as_text()
            data = json.loads(content)

            venue_name = data.get("venueName", "Unknown")  # Default to 'Unknown' if missing
            records = data.get("data", [])

            if records:
                # Add VenueName to each record
                for record in records:
                    record["VenueName"] = venue_name

                all_records.extend(records)
                print(f"✅ Added {len(records)} records from {blob.name}")
            else:
                print(f"⚠️ No data found in {blob.name}")

        except Exception as e:
            print(f"❌ Failed to process {blob.name}: {e}")

# Convert to DataFrame
df = pd.DataFrame(all_records)

# Select required columns including VenueName
required_cols = ["TransactionDate", "TransID","POS_Terminal_Description", "TenderDescription","Customer_Type_Description", "SalesAmount", "BankingAmount"]
existing_cols = [col for col in required_cols if col in df.columns]
df_filtered = df[existing_cols]

# Save to CSV
df_filtered.to_csv('/Users/apple/Documents/Project/quantaco_testing/20250405_116.csv', index=False)

print("\n✅ All data has been written to df_filtered.to_csv")