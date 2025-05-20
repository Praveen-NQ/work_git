import os
import json
import pandas as pd
from google.cloud import storage

# Auth setup
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/apple/.config/gcloud/application_default_credentials.json"

# Input parameters
id = '128'
output_file = f'/Users/apple/Documents/project/work_git/quantaco_testing/AHB_all_tenders_2.csv'

# GCS client setup
client = storage.Client()
bucket = client.get_bucket('bepoz')

# Prefix to filter files
date_prefix = f'{id}/Australian Hotel Ballina_20250417'
blobs = bucket.list_blobs(prefix=date_prefix)

# Store all matching records
all_records = []

# Loop through each JSON blob
for blob in blobs:
    if blob.name.endswith('.json') and blob.name.startswith(date_prefix):
        print(f"📂 Processing file: {blob.name}")
        try:
            content = blob.download_as_text()
            data = json.loads(content)

            venues = data if isinstance(data, list) else [data]

            for venue in venues:
                for store in venue.get("Stores", []):
                    for txn in store.get("Transactions", []):
                        #if txn.get("TillName") != "SHB Bistro 1":
                           # continue
                        for item in txn.get("Items", []):
                            product = item.get("Product", {})
                            category = product.get("Category", "")
                            # Uncomment the line below if you still want to filter only 'Food' items
                            # if "Food" in category:
                            payments = txn.get("Payments", [])
                            if not payments:
                                record = {
                                    "BlobName": blob.name,
                                    "Venue": venue.get("VenueName"),
                                    "LineID": item.get("LineID"),
                                    "TransactionID": txn.get("TransactionID"),
                                    "TransactionType": txn.get("TransactionType"),
                                    "Transactioned_at": txn.get("DateTimeUTC"),
                                    "TillName": txn.get("TillName"),
                                    "TotaliserName": None,                                  
                                    "Quantity": item.get("Quantity"),
                                    #"Amount": item.get("NettPrice"),
                                    "Category": category,
                                    "CategoryGroupID": product.get("CategoryGroupID"),
                                    "CategoryGroup": product.get("CategoryGroup"),
                                    "PaymentName": None,
                                    "PaymentAmount": None
                                }
                                all_records.append(record)
                            else:
                                for payment in payments:
                                    record = {
                                        "BlobName": blob.name,
                                        "Venue": venue.get("VenueName"),
                                        "LineID": item.get("LineID"),
                                        "TransactionID": txn.get("TransactionID"),
                                        "TransactionType": txn.get("TransactionType"),
                                        "Transactioned_at": txn.get("DateTimeUTC"),
                                        "TillName": txn.get("TillName"),
                                        "TotaliserName": None,
                                        "Quantity": item.get("Quantity"),
                                        #"Amount": item.get("NettPrice"),
                                        "Category": category,
                                        "CategoryGroupID": product.get("CategoryGroupID"),
                                        "CategoryGroup": product.get("CategoryGroup"),
                                        "PaymentName": payment.get("Name"),
                                        "PaymentAmount": payment.get("Amount")
                                    }
                                    all_records.append(record)


        except json.JSONDecodeError as e:
            print(f"❌ Failed to decode JSON in {blob.name}: {e}")
        except Exception as e:
            print(f"⚠️ Error in {blob.name}: {e}")

# ✅ Save output
if all_records:
    df = pd.DataFrame(all_records)
    df.to_csv(output_file, index=False)
    print(f"\n✅ Saved {len(df)} records to {output_file}")
else:
    print("\n❗ No matching records with TillName = 'SHB Bistro 1' found.")
## tender wise 