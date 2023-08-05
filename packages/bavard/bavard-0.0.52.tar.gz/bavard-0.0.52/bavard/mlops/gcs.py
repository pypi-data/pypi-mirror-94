"""Google Cloud Storage (GCS) utilities.
"""
from bavard_ml_common.mlops.gcs import GCSClient


def download_agent_data(bucket_name, export_file_key) -> str:
    storage_client = GCSClient()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(export_file_key)
    filename = '/tmp/agent_data.json'
    blob.download_to_filename(filename)
    return filename
