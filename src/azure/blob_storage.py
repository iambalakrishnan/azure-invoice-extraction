import os
from azure.storage.blob import BlobServiceClient, ContainerClient

def get_blob_service_client():
    connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    return BlobServiceClient.from_connection_string(connection_string)

def get_container_client(container_name):
    blob_service_client = get_blob_service_client()
    return blob_service_client.get_container_client(container_name)

def get_blobs_in_directory(container_client, directory_name):
    blobs = container_client.list_blobs(name_starts_with=directory_name)
    return [blob for blob in blobs if not blob.name.endswith("/")]  # Exclude subdirectories

def move_blob(container_client, source_blob_name, dest_blob_name):
    source_blob = container_client.get_blob_client(source_blob_name)
    dest_blob = container_client.get_blob_client(dest_blob_name)

    dest_blob.start_copy_from_url(source_blob.url)
    source_blob.delete_blob()
