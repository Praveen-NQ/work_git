import os
import json
import pandas as pd
from datetime import datetime
from google.cloud import storage

# Auth setup
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/apple/.config/gcloud/application_default_credentials.json"

# GCS setup
storage_client = storage.Client()
bucket_name = 'bepoz'
bucket = storage_client.bucket(bucket_name)

# List all files in the bucket with a specific prefix
prefix = '128/Australian Hotel Ballina_20250417'
blobs = bucket.list_blobs(prefix=prefix)
file_list = [blob.name for blob in blobs if blob.name.endswith('.json')]

all_records = []

# Process files
for file in file_list:
    print(f"📂 Processing file: {file}")
    blob = bucket.blob(file)
    with blob.open("r") as f:
        content = f.read()
        content = json.loads(content)
        venue = content[0]
        venue_name = venue.get("VenueName")

        for store in venue.get("Stores", []):
            for transaction in store.get("Transactions", []):
                transaction_id = transaction.get("TransactionID")
                transaction_type = transaction.get("TransactionType")
                area_name = transaction.get("TillName")
                till_name = transaction.get("TillName")
                txn_datetime_str = transaction.get("DateTimeUTC")
                try:
                    txn_datetime = datetime.strptime(txn_datetime_str, '%d/%m/%Y %I:%M:%S %p')
                except:
                    txn_datetime = None

                txn_datetime_fmt = txn_datetime.strftime('%Y-%m-%dT%H:%M:%S') if txn_datetime else txn_datetime_str

                # Order Discount & Service Charge
                for category_name, amount in {
                    "Order Discount": transaction.get("OrderDiscount", 0.0),
                    "Service Charge": transaction.get("ServiceCharge", 0.0)
                }.items():
                    all_records.append({
                        "record_type": "Discount",
                        "venue_name": venue_name,
                        "area_name": area_name,
                        "till_name": till_name,
                        "transaction_id": transaction_id,
                        "line_no": None,
                        "transaction_datetime": txn_datetime,
                        "transaction_datetime_str": txn_datetime_fmt,
                        "transaction_type": transaction_type,
                        "category_name": category_name,
                        "category_group_name": category_name,
                        "nettotal": amount,
                        "tender_name": None,
                        "tender_amount": None
                    })

                # Items
                for item in transaction.get("Items", []):
                    product = item.get("Product", {})
                    all_records.append({
                        "record_type": "Item",
                        "venue_name": venue_name,
                        "area_name": area_name,
                        "till_name": till_name,
                        "transaction_id": transaction_id,
                        "line_no": item.get("LineID"),
                        "transaction_datetime": txn_datetime,
                        "transaction_datetime_str": txn_datetime_fmt,
                        "transaction_type": transaction_type,
                        "category_name": product.get("Category"),
                        "category_group_name": product.get("CategoryGroup"),
                        "nettotal": item.get("NettTotal"),
                        "tender_name": None,
                        "tender_amount": None
                    })

                # Payments (Tenders)
                for i, payment in enumerate(transaction.get("Payments", []), start=1):
                    all_records.append({
                        "record_type": "Tender",
                        "venue_name": venue_name,
                        "area_name": area_name,
                        "till_name": till_name,
                        "transaction_id": transaction_id,
                        "line_no": i,
                        "transaction_datetime": txn_datetime,
                        "transaction_datetime_str": txn_datetime_fmt,
                        "transaction_type": transaction_type,
                        "category_name": None,
                        "category_group_name": None,
                        "nettotal": None,
                        "tender_name": payment.get("Name"),
                        "tender_amount": payment.get("Amount")
                    })

# ✅ Convert to DataFrame
df = pd.DataFrame(all_records)

# 🔁 Drop duplicates
df = df.drop_duplicates(subset=['venue_name', 'transaction_id', 'line_no'])

# 💾 Save to CSV
output_path = "/Users/apple/Documents/project/work_git/quantaco_testing/AHB_all_tenders_cleaned.csv"
df.to_csv(output_path, index=False)

print(f"\n✅ Saved {len(df)} unique records to: {output_path}")