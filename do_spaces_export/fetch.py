"""List or download objects from S3 Bucket,"""
from log import LOGGER


def list_objects_in_bucket(client, bucket_name: str):
    """
    List all objects in bucket directory.

    :param ServiceResource client: Session client with DO Spaces.
    :param bucket_name: Name of bucket to fetch objects from.
    """
    all_objects = []
    continuation_token = None

    while True:
        if continuation_token:
            response = client.list_objects_v2(
                Bucket=bucket_name,
                ContinuationToken=continuation_token
            )
        else:
            response = client.list_objects_v2(Bucket=bucket_name)

        if "Contents" in response:
            all_objects.extend(response["Contents"])
            LOGGER.info(
                f"Fetched {len(response['Contents'])} objects (total: {len(all_objects)})"
            )

        # Check if there are more objects to fetch
        if response.get("IsTruncated"):
            continuation_token = response.get("NextContinuationToken")
        else:
            break

    LOGGER.info(
        f"Fetched {len(all_objects)} total objects from bucket `{bucket_name}`"
    )
    return all_objects


