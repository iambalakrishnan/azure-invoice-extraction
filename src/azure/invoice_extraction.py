import os
import logging
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient


logger = logging.getLogger(__name__)


def get_document_analysis_client():
    endpoint = os.getenv("DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("DOCUMENT_INTELLIGENCE_KEY")
    return DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))


def extract_invoice_data(blob):
    try:
        document_analysis_client = get_document_analysis_client()
        logger.info(f"Extracting invoice data from blob: {blob.name}")

        with blob.download_blob() as invoice_stream:
            poller = document_analysis_client.begin_analyze_document("prebuilt-invoice", invoice_stream)
        invoices = poller.result()

        if not invoices.documents:
            logger.warning(f"No documents found in blob: {blob.name}")
            return None

        extracted_data = []

        for idx, invoice in enumerate(invoices.documents):
            logger.info(f"Analyzing invoice #{idx + 1}")
            invoice_dict = {}
            for name, field in invoice.fields.items():
                if name == "Items":
                    invoice_dict[name] = []
                    for item in field.value:
                        item_dict = {}
                        for item_name, item_field in item.value.items():
                            item_dict[item_name] = item_field.value
                        invoice_dict[name].append(item_dict)
                else:
                    invoice_dict[name] = field.value if field.value else None  # Handle missing values
            extracted_data.append(invoice_dict)

        logger.info(f"Extracted data: {extracted_data}")
        return extracted_data
    except Exception as e:
        logger.error(f"Error extracting invoice data from blob: {blob.name} - {e}")
        raise

