"""Initialize script."""
from config import DO_STORAGE_BUCKET_NAME, EXPORT_DIRECTORY_FILEPATH
from do_spaces_export.client import create_client
from do_spaces_export.fetch import list_objects_in_bucket
from do_spaces_export.export import download_objects, create_directories, get_download_log
from log import LOGGER


def init_script():
    """Download all objects in bucket with resume capability."""
    try:
        client = create_client()
        
        # Check for existing progress
        existing_log = get_download_log(EXPORT_DIRECTORY_FILEPATH)
        if existing_log:
            LOGGER.info(f"Resuming download. {len(existing_log)} files already downloaded.")
        
        objects = list_objects_in_bucket(client, DO_STORAGE_BUCKET_NAME)
        files = [file for file in objects if file["Key"][-1] != "/"]
        directories = [dir for dir in objects if dir["Key"][-1] == "/"]
        
        LOGGER.info(f"Total files in bucket: {len(files)}")
        
        create_directories(directories, EXPORT_DIRECTORY_FILEPATH)
        stats = download_objects(client, files, DO_STORAGE_BUCKET_NAME, EXPORT_DIRECTORY_FILEPATH)
        
        # Print summary
        LOGGER.success(f"\n=== Download Summary ===")
        LOGGER.success(f"Downloaded: {stats['downloaded']}")
        LOGGER.info(f"Skipped (already logged): {stats['skipped_logged']}")
        LOGGER.info(f"Skipped (file exists): {stats['skipped_exists']}")
        if stats['failed'] > 0:
            LOGGER.warning(f"Failed: {stats['failed']}")
        LOGGER.success(f"Total processed: {len(files)}")
        
    except KeyboardInterrupt:
        LOGGER.info("\nExiting. Run the script again to resume.")
    except Exception as e:
        LOGGER.error(f"Error occurred while attempting to download objects: {e}")
