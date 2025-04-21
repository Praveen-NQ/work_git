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
date_prefix = ['116/2025-04-04', '116/2025-04-05']  # Adjust date here

all_records = []

blobs = bucket.list_blobs(prefix=date_prefix)

# Loop through each file
for blob in blobs: