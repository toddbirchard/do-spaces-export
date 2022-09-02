"""Initialize script."""
from config import DO_STORAGE_BUCKET_NAME, EXPORT_DIRECTORY_FILEPATH
from do_spaces_export.client import create_client
from do_spaces_export.fetch import list_objects_in_bucket
from do_spaces_export.export import download_objects, create_directories
from log import LOGGER


def init_script():
    """Download all objects in bucket."""
    try:
        client = create_client()
        objects = list_objects_in_bucket(client, DO_STORAGE_BUCKET_NAME)
        files = [file for file in objects if file["Key"][-1] != "/"]
        directories = [dir for dir in objects if dir["Key"][-1] == "/"]
        create_directories(directories, EXPORT_DIRECTORY_FILEPATH)
        download_objects(client, files, DO_STORAGE_BUCKET_NAME, EXPORT_DIRECTORY_FILEPATH)
        LOGGER.success(f"Successfully downloaded {len(files)}")
    except Exception as e:
        LOGGER.error(f"Error occurred while attempting to download objects: {e}")
