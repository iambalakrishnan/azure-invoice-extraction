import os
import json
from azure.cosmos import CosmosClient, PartitionKey, exceptions
import logging

logger = logging.getLogger(__name__)

def get_cosmos_client():
    """Creates and returns a CosmosClient instance."""
    endpoint = os.getenv("COSMOSDB_ENDPOINT")
    key = os.getenv("COSMOSDB_KEY")
    try:
        return CosmosClient(endpoint, key)
    except exceptions.CosmosHttpResponseError as e:
        logger.error(f"Error connecting to Cosmos DB: {e}")
        raise  # Re-raise the exception for higher-level handling

def store_invoice_data(invoice_data):
    """Stores the extracted invoice data into Cosmos DB."""
    try:
        client = get_cosmos_client()
        database_name = os.getenv("COSMOSDB_DATABASE_NAME")
        container_name = os.getenv("COSMOSDB_CONTAINER_NAME")

        database = client.get_database_client(database_name)
        container = database.get_container_client(container_name)

        # Ensure container exists, create if not
        try:
            container.read()
        except exceptions.CosmosResourceNotFoundError:
            logger.warning(f"Container '{container_name}' not found, creating...")
            database.create_container(id=container_name, partition_key=PartitionKey(path="/InvoiceId"))
            container = database.get_container_client(container_name)

        for invoice in invoice_data:
            # Generate a unique ID (consider using a UUID library if needed)
            item_id = invoice.get("InvoiceId", "unknown_invoice_id")  

            # Create the item
            item = {
                "id": item_id,  
                "partitionKey": item_id,  # Partition key usually matches the ID for invoices
                "data": invoice,
            }

            container.upsert_item(item)
            logger.info(f"Stored invoice data in Cosmos DB with ID: {item_id}")

    except Exception as e:
        logger.error(f"Error storing invoice data in Cosmos DB: {e}")
        raise
