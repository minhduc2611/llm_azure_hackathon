import os
from dotenv import load_dotenv
from azure.storage.blob import BlobSasPermissions, generate_blob_sas, BlobServiceClient
from datetime import datetime, timedelta
import os
# Load environment variables
load_dotenv()

# Load config from .env
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_STORAGE_CONTAINER = os.getenv("AZURE_STORAGE_CONTAINER")
AZURE_STORAGE_ACCOUNT = os.getenv("AZURE_STORAGE_ACCOUNT")

def upload_file_to_blob(file_stream, blob_name: str, id: str = None) -> tuple[str, str]:
    """
    Uploads a file stream to a private Azure Blob container.

    Args:
        file_stream (IO): File-like object (e.g. from request.files[i].stream).
        blob_name (str): The name of the blob (e.g. filename).
        id (str): Optional folder prefix (e.g. user ID or group ID).

    Returns:
        tuple[str, str]: Tuple of blob path and full blob URL.
    """
    # Build the blob path with optional folder prefix
    id = id or "default"
    blob_path = f"{id}/{blob_name}"

    # Create Azure blob client
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER)

    # Upload the file stream to the container
    container_client.upload_blob(name=blob_path, data=file_stream, overwrite=True)

    # Construct the blob URL (not public without a SAS token)
    blob_url = f"https://{AZURE_STORAGE_ACCOUNT}.blob.core.windows.net/{AZURE_STORAGE_CONTAINER}/{blob_path}"

    return blob_path, blob_url



def get_signed_url(blob_path: str, expiry_minutes: int = 60) -> tuple[str, int, int]:
    """
    Generates a signed URL for a blob in Azure Blob Storage.

    Args:
        blob_path (str): The path of the blob.
        expiry_minutes (int): The number of minutes the URL will be valid.

    Returns:
        str: The signed URL for the blob.
    """
    sas_token = generate_blob_sas(
        account_name=os.getenv("AZURE_STORAGE_ACCOUNT"),
        container_name=os.getenv("AZURE_STORAGE_CONTAINER"),
        blob_name=blob_path,
        account_key=os.getenv("AZURE_STORAGE_ACCOUNT_KEY"),
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(minutes=expiry_minutes)
    )
    
    url = f"https://{os.getenv('AZURE_STORAGE_ACCOUNT')}.blob.core.windows.net/{os.getenv('AZURE_STORAGE_CONTAINER')}/{blob_path}?{sas_token}"
    # time format to milliseconds
    expiry_date = datetime.now() + timedelta(minutes=expiry_minutes)
    expiry_date_ms = int(expiry_date.timestamp() * 1000)
    return url, expiry_minutes, expiry_date_ms 