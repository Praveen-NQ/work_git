import os
import json
import pandas as pd # type: ignore
from google.cloud import storage

# Auth setup
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/apple/.config/gcloud/application_default_credentials.json"

id = ''
start_date = ''
output_file = f''
pos_type = ''
# GCS client setup
client = storage.Client()
bucket = client.get_bucket(f'{pos_type}')

# Prefix to filter files
date_prefix = f'{id}/{start_date}'
blobs = bucket.list_blobs(prefix=date_prefix)

all_records = []