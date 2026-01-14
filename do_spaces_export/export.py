"""List or download objects from S3 Bucket,"""
import os
import json
from pathlib import Path
from typing import List, Set
from botocore.exceptions import ClientError

from log import LOGGER

# Log file to track downloaded files
DOWNLOAD_LOG_FILE = "download_log.json"


def get_download_log(local_path: str) -> Set[str]:
    """
    Load the download log from disk.

    :param str local_path: Local path where the log file is stored.
    :returns: Set of already downloaded file keys.
    """
    log_filepath = f"{local_path}/{DOWNLOAD_LOG_FILE}"
    if os.path.exists(log_filepath):
        try:
            with open(log_filepath, "r") as f:
                data = json.load(f)
                return set(data.get("downloaded_files", []))
        except (json.JSONDecodeError, Exception) as e:
            LOGGER.warning(f"Could not read download log: {e}. Starting fresh.")
    return set()


def save_download_log(local_path: str, downloaded_files: Set[str]) -> None:
    """
    Save the download log to disk.

    :param str local_path: Local path where the log file is stored.
    :param Set[str] downloaded_files: Set of downloaded file keys.
    """
    log_filepath = f"{local_path}/{DOWNLOAD_LOG_FILE}"
    os.makedirs(local_path, exist_ok=True)
    with open(log_filepath, "w") as f:
        json.dump({"downloaded_files": list(downloaded_files)}, f, indent=2)


def add_to_download_log(local_path: str, file_key: str, downloaded_files: Set[str]) -> None:
    """
    Add a file to the download log and save immediately.

    :param str local_path: Local path where the log file is stored.
    :param str file_key: The file key to add.
    :param Set[str] downloaded_files: Set of downloaded file keys.
    """
    downloaded_files.add(file_key)
    save_download_log(local_path, downloaded_files)


def create_directories(directories: list, local_filepath: str) -> None:
    """
    Create directories in export directory.

    :param list directories: List of directories to create.
    """
    try:
        os.makedirs(local_filepath, exist_ok=True)
        for directory in directories:
            directory_path = f"{local_filepath}/{directory['Key']}"
            LOGGER.info(f"Creating directory `{directory_path}`")
            os.makedirs(directory_path, exist_ok=True)
    except Exception as e:
        raise e


def download_objects(
    client, files: List[str], bucket_name: str, local_path: str
) -> dict:
    """
    Download files from an S3 bucket with resume capability.

    :param Service client: S3 transfer client.
    :param List[str] files: Files to download from remote bucket.
    :param str bucket_name: Name of S3 bucket to fetch from.
    :param str local_path: Local path to download files to.

    :returns: dict with download statistics.
    """
    # Load existing download log
    downloaded_files = get_download_log(local_path)
    
    stats = {
        "downloaded": 0,
        "skipped_exists": 0,
        "skipped_logged": 0,
        "failed": 0
    }
    
    total_files = len(files)
    
    try:
        for index, file in enumerate(files, 1):
            file_key = file["Key"]
            local_filepath = f"{local_path}/{file_key}"
            
            # Skip if already in download log
            if file_key in downloaded_files:
                LOGGER.info(f"[{index}/{total_files}] Skipping (already logged): {file_key}")
                stats["skipped_logged"] += 1
                continue
            
            # Skip if file already exists on disk
            if os.path.exists(local_filepath):
                LOGGER.info(f"[{index}/{total_files}] Skipping (file exists): {file_key}")
                # Add to log since it exists
                add_to_download_log(local_path, file_key, downloaded_files)
                stats["skipped_exists"] += 1
                continue
            
            # Create parent directories if they don't exist
            os.makedirs(os.path.dirname(local_filepath), exist_ok=True)
            
            try:
                with open(local_filepath, "wb") as f:
                    client.download_fileobj(bucket_name, file_key, f)
                
                # Add to download log immediately after successful download
                add_to_download_log(local_path, file_key, downloaded_files)
                
                LOGGER.success(
                    f"[{index}/{total_files}] Downloaded: {file_key}"
                )
                stats["downloaded"] += 1
                
            except Exception as e:
                LOGGER.error(f"[{index}/{total_files}] Failed to download {file_key}: {e}")
                stats["failed"] += 1
                # Remove partial file if it exists
                if os.path.exists(local_filepath):
                    os.remove(local_filepath)
                continue
                
    except KeyboardInterrupt:
        LOGGER.warning("\nDownload interrupted by user. Progress has been saved.")
        LOGGER.info(f"Resume by running the script again. {len(downloaded_files)} files logged.")
        raise
    
    return stats
