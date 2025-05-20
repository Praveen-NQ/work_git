import os
import json
from google.cloud import storage

# Set up GCP auth
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/apple/.config/gcloud/application_default_credentials.json"

# Function to print required fields if Category contains "%Food%"
def print_category_info(content):
    try:
        data = json.loads(content)
        if isinstance(data, dict):  # If the JSON is a dictionary
            records = data.get("data", [])
        elif isinstance(data, list):  # If the JSON is a list
            records = data
        else:
            print("⚠️ JSON content is neither a dictionary nor a list.")
            return

        # Process records if they exist
        for record in records:
            if isinstance(record, dict) and "Category" in record and "%Food%" in record["Category"]:
                print(f"Category: {record['Category']}")
                print(f"CategoryGroupID: {record['CategoryGroupID']}")
                print(f"CategoryGroup: {record['CategoryGroup']}")
                print("-" * 40)
    except json.JSONDecodeError as e:
        print(f"❌ Failed to decode JSON: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ Failed to decode JSON: {e}")

# Main function to get and process blobs
def print_all_blob_contents(pos_type, id, start_date):
    client = storage.Client()
    bucket = client.get_bucket(pos_type)
    prefix = f"{id}/{start_date}"
    blobs = bucket.list_blobs(prefix=prefix)

    for blob in blobs:
        content = blob.download_as_text()
        print(f"\n📄 Blob Name: {blob.name}")
        print_category_info(content)

# Example usage
print_all_blob_contents("bepoz", "128", "Southern Hotel Berry_20250427")