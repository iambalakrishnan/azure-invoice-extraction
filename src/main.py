import os
import json
from dotenv import load_dotenv
import logging
from src.azure import blob_storage, invoice_extraction, cosmosdb
from logger import get_logger

load_dotenv()

logger = get_logger(__name__)

def main():
    try:
        # Fetch unprocessed invoices
        container_client = blob_storage.get_container_client(os.getenv("BLOB_STORAGE_CONTAINER_NAME"))
        unprocessed_blobs = blob_storage.get_blobs_in_directory(container_client, "unprocessed/")
        logger.info("Started processing invoices")
        for blob in unprocessed_blobs:
            try:
                logger.info(f"Processing invoice: {blob.name}")
                # Extract data
                invoice_data = invoice_extraction.extract_invoice_data(blob)

                # Store locally in JSON format
                if invoice_data:
                    with open(os.path.join("data", f"{blob.name}.json"), "w") as f:
                        json.dump(invoice_data, f, indent=4)
                    logger.info(f"Data from {blob.name} stored locally.")

                # Store in Cosmos DB (only if data was extracted)
                if invoice_data:  
                    cosmosdb.store_invoice_data(invoice_data)

                # Move to processed directory
                blob_storage.move_blob(container_client, blob.name, "processed/")
                logger.info(f"Processed and moved invoice: {blob.name}")

            except Exception as e:
                logger.error(f"Error processing invoice {blob.name}: {e}")
        logger.info("Finished processing invoices")
    except Exception as e:
        logger.critical(f"Critical error: {e}")
        raise


if __name__ == "__main__":
    main()
