import os
import json
import pandas as pd
from google.cloud import storage

# Auth setup
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/apple/.config/gcloud/application_default_credentials.json"

id = '2'
output_file = f'/Users/apple/Documents/project/work_git/quantaco_testing/202504_{id}.csv'

# GCS client setup
client = storage.Client()
bucket = client.get_bucket('idealpos-upload-payments')

# Prefix to filter files
date_prefix = f'{id}/2025-04'
blobs = bucket.list_blobs(prefix=date_prefix)

all_records = []

# Loop through each file
for blob in blobs:
    if blob.name.endswith('.json') and blob.name.startswith(date_prefix):
        print(f"📂 Processing file: {blob.name}")
        try:
            content = blob.download_as_text()
            data = json.loads(content)

            venue_name = data.get("venueName", "Unknown")
            venue_id = data.get("venueId", "Unknown")  # Assuming 'venueId' is present in JSON
            records = data.get("data", [])

            if records:
                for record in records:
                    record["VenueName"] = venue_name
                    record["Venue_ID"] = venue_id
                    record["SourceFile"] = blob.name  # Add filename to track source
                    if record.get("SalesAmount") != record.get("BankingAmount"):
                        all_records.append(record)
                print(f"✅ Added {len(records)} records from {blob.name}")
            else:
                print(f"⚠️ No data found in {blob.name}")
        except Exception as e:
            print(f"❌ Failed to process {blob.name}: {e}")

# Convert to DataFrame
df = pd.DataFrame(all_records)

# Select required columns
required_cols = ["SourceFile", "Venue_ID", "TransactionDate", "TransID", "POS_Terminal_Description",
                 "TenderDescription", "Customer_Type_Description", "SalesAmount", "BankingAmount", "VenueName"]
existing_cols = [col for col in required_cols if col in df.columns]
df_filtered = df[existing_cols]

# Save to CSV
df_filtered.to_csv(output_file, index=False)
print(f"\n✅ All data has been written to {output_file}")