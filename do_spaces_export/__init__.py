"""Initialize script."""
from config import DO_STORAGE_BUCKET_NAME
from do_spaces_export.client import create_client
from do_spaces_export.fetch import download_object, list_objects_in_bucket
from log import LOGGER


def init_script():
    """Download all objects in bucket."""
    try:
        client = create_client()
        files = list_objects_in_bucket(client, DO_STORAGE_BUCKET_NAME)
        files = [file for file in files if file["Key"][-1] != "/"]
        for file in files:
            download_object(client, file["Key"], DO_STORAGE_BUCKET_NAME)
        LOGGER.success(f"Successfully downloaded {len(files)}")
    except Exception as e:
        LOGGER.error(f"Error occurred while attempting to download objects: {e}")
