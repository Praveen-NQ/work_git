import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/apple/.config/gcloud/application_default_credentials.json"
from google.cloud import storage
from google.cloud import bigquery

def get_gcs_object_details(bucket_name): 
    """
    Get the object details from a GCS bucket.
    """
    client = storage.Client()
    blobs = client.list_blobs(bucket_name)
    object_details = []
    for blob in blobs:
        object_details.append({
            'name': blob.name,
            'size': blob.size,
            'updated': blob.updated
        })
    return object_details


#conda create -n gcp_connect python=3.12.9 -y