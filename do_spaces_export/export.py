"""List or download objects from S3 Bucket,"""
import os
from pathlib import Path
from typing import List
from botocore.exceptions import ClientError

from log import LOGGER


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
) -> None:
    """
    Download files from an S3 bucket.

    :param Service client: S3 transfer client.
    :param List[str] files: Files to download from remote bucket.
    :param str bucket_name: Name of S3 bucket to fetch from.
    :param str local_path: Local path to download files to.

    :returns: None
    """
    try:
        for file in files:
            local_filepath = f"{local_path}/{file['Key']}"
            with open(local_filepath, "wb") as f:
                client.download_fileobj(bucket_name, file["Key"], f)
                LOGGER.success(
                    f"Fetched file `{file['Key']}` from bucket `{bucket_name}`"
                )
    except ClientError as e:
        raise e
    except Exception as e:
        raise e
