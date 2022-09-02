"""Script configuration."""
from os import getenv, path

from dotenv import load_dotenv

# Load variables from .env
BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

DO_STORAGE_REGION_NAME = getenv("DO_STORAGE_REGION_NAME")
DO_STORAGE_SPACE_URL = "https://nyc3.digitaloceanspaces.com"
DO_STORAGE_KEY_ID = getenv("DO_STORAGE_KEY_ID")
DO_STORAGE_KEY_SECRET = getenv("DO_STORAGE_KEY_SECRET")
DO_STORAGE_BUCKET_NAME = getenv("DO_STORAGE_BUCKET_NAME")

EXPORT_DIRECTORY_FILEPATH = f"{BASE_DIR}/export/{DO_STORAGE_BUCKET_NAME}"
