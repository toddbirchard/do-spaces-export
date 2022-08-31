"""Initialize session client with DO Spaces."""
import boto3
from boto3.session import Session

from config import DO_STORAGE_KEY_ID, DO_STORAGE_KEY_SECRET


def create_client() -> Session:
    """
    Create session client with DO Spaces.

    :returns: Session
    """
    session = boto3.session.Session()
    client = session.client(
        "s3",
        region_name="nyc3",
        endpoint_url="https://nyc3.digitaloceanspaces.com",
        aws_access_key_id=DO_STORAGE_KEY_ID,
        aws_secret_access_key=DO_STORAGE_KEY_SECRET,
    )
    return client
