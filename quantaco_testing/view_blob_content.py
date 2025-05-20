import os
from google.cloud import storage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/apple/.config/gcloud/application_default_credentials.json"

def print_all_blob_contents(pos_type, id, start_date):
    client = storage.Client()
    bucket = client.get_bucket(pos_type)
    prefix = f"{id}/{start_date}"
    blobs = bucket.list_blobs(prefix=prefix)

    for blob in blobs:
        content = blob.download_as_text()
        print(f"\n📄 Blob Name: {blob.name}")
        print("Content:\n", content)

# Example call
print_all_blob_contents("bepoz", "128", "Southern Hotel Berry_20250427")
