import os
import json
import joblib
import pandas as pd

from google.cloud import storage
from google.oauth2 import service_account

PROJECT_ID = "daring-avenue-297414"
BUCKET_NAME = "practical_blackwell"


def get_credentials():  
    credentials_raw = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if ".json" in credentials_raw:
        credentials_raw = open(credentials_raw).read()
    creds_json = json.loads(credentials_raw)
    greds_gcp = service_account.Credentials.from_service_account_info(creds_json)
    return greds_gcp

def get_movie_name_lst():
    filename = "name_lst.joblib"
    if os.path.exists(f"{filename}"):
        print("File exists.")
    else:
        creds = get_credentials()
        client = storage.Client(credentials=creds, project=PROJECT_ID).bucket(BUCKET_NAME)   
        storage_location = f"movie/{filename}"
        blob = client.blob(storage_location)
        blob.download_to_filename(f"{filename}")
        print(f"{filename} saved.")
    name_lst=joblib.load(f"{filename}")
    os.remove(f"{filename}")
    print(f"{filename} deleted.")
    return name_lst
