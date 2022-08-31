"""List or download objects from S3 Bucket,"""
from botocore.exceptions import ClientError

from config import EXPORT_DIRECTORY_FILEPATH
from log import LOGGER


def list_objects_in_bucket(client, bucket_name: str):
    """
    List all objects in bucket directory.

    :param ServiceResource client: Session client with DO Spaces.
    :param bucket_name: Name of bucket to fetch objects from.
    """
    response = client.list_objects(Bucket=bucket_name)
    LOGGER.info(
        f"Fetched {len(response['Contents'])} objects from bucket `{bucket_name}`"
    )
    return response["Contents"]


def download_object(client, filename, bucket_name: str) -> None:
    """
    Download file from an S3 bucket.

    :param Service client: S3 transfer client.
    :param str filename: Remote filename of object (including path).
    :param str bucket_name: Name of S3 bucket to fetch from.

    :returns: None
    """
    try:
        with open(f"{EXPORT_DIRECTORY_FILEPATH}/{filename}", "wb") as f:
            client.download_fileobj(bucket_name, filename, f)
            LOGGER.success(f"Fetched file {filename} from {bucket_name}")
    except ClientError as e:
        raise e
    except Exception as e:
        raise e
