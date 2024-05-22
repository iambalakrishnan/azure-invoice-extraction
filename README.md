# azure-invoice-extraction
Extract invoices using azure prebuilt extraction model

# Azure Invoice Processor

This Python project automates the extraction of data from PDF invoices stored in Azure Blob Storage using Azure Document Intelligence (formerly Form Recognizer). Extracted data is stored in both local JSON files and Azure Cosmos DB for further processing and analysis.

## Features

- **Automated Processing:** Scans a specified directory in Azure Blob Storage for unprocessed invoices.
- **Document Intelligence:** Utilizes Azure's prebuilt invoice extraction model for accurate data extraction.
- **Local Storage:** Stores extracted invoice data as JSON files for convenient access.
- **Cosmos DB Integration:** Saves extracted data to Azure Cosmos DB for structured storage and querying.
- **Blob Management:** Moves processed invoices to a "processed" directory in Blob Storage.
- **Robust Logging:** Logs processing steps, errors, and key information for easy monitoring and troubleshooting.
- **Modular Design:** Organized into separate modules (`azure`, `logger`) for maintainability and reusability.
- **Dockerized:** Packaged as a Docker container for seamless deployment and portability.

## Prerequisites

- **Azure Account:**  You need an active Azure subscription with the following resources:
  - **Blob Storage Account:** To store your invoices.
  - **Document Intelligence Resource:** To perform invoice extraction.
  - **Cosmos DB Account:** To store extracted data.
- **Python 3.9 or higher:** Install Python on your local machine.
- **Docker:** (Optional) For containerized deployment.

## Setup

1. **Clone Repository:** `git clone https://github.com/iambalakrishnan/azure-invoice-extraction.git`
2. **Environment Variables:** Create a `.env` file in the project root and set the following variables with your Azure credentials and settings:
3. **Dependencies:** Install the required packages using pip: `pip install -r requirements.txt` 

## Running the Project

### Local Execution:

1. **Upload Invoices:**  Upload PDF invoices to the `unprocessed` directory in your Azure Blob Storage container.
2. **Run Script:** `python src/main.py`
3. **Output:** Extracted data will be saved as JSON files in the `data` directory.

### Docker Execution (Recommended):

1. **Build Image:** `docker build -t invoice-processor .`
2. **Run Container:** `docker run invoice-processor`


## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the [MIT License](LICENSE).