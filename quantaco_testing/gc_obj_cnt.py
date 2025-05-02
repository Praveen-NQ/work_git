import os
from google.cloud import storage

# Auth setup
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/apple/.config/gcloud/application_default_credentials.json"

# Set ID and date
id = '9'

# GCS client setup
client = storage.Client()
bucket = client.get_bucket('idealpos-upload-payments')

# Combine prefix (e.g., '9/2025-04-05/')
date_prefix = f'{id}/2025-04'  # Use f-string here too

def get_blob_count_and_size(bucket, prefix):
    """
    Count the number of blobs and calculate their total size in bytes.
    """
    blobs = bucket.list_blobs(prefix=date_prefix)
    count = 0
    total_size = 0

    for blob in bucket.list_blobs():
        if blob.name.endswith('.json') and blob.name.startswith(date_prefix):
            count += 1
            total_size += blob.size
            print(f"Blob: {blob.name}, Size: {blob.size / (1024 * 1024):.2f} MB")


    return count, total_size

# Call the function
blob_count, total_blob_size = get_blob_count_and_size(bucket, date_prefix)

# Output result
print(f"📦 Total blobs with prefix '{date_prefix}': {blob_count}")
print(f"📏 Total size: {total_blob_size / (1024 * 1024):.2f} MB")