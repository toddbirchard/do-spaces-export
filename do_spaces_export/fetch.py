"""List or download objects from S3 Bucket,"""
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


