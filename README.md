# Dole Intelligent Document Processing API

This project provides an API for document intelligence, allowing users to analyze and extract information from file types like PDF to JSON or TXT format.

## Dependencies

To run this program, you need the following dependencies:

- Python 3.13 or higher ([download here!](https://www.python.org/downloads/))
- 
- `configparser`
- `aiohttp`
- `asyncio`
- `azure-core`
- `azure-ai-documentintelligence`
- `azure-storage-blob`

You can install the required Python packages using pip:
```sh
pip install os configparser json asyncio azure-core azure-ai-documentintelligence azure-storage-blob
```

## Configuration

Create a `config.ini` file in the root directory of the project with the following content:

```ini
[DEFAULT]
api_key = your_azure_api_key_here
endpoint = https://endpointname.azure.com/
pdf_api_container = https://blobstoragename.blob.core.windows.net/key
pdf_output_container = https://blobstoragename.blob.core.windows.net/key
output_file_path = your/path/here
```

For more info on how to use Azure blobs, [go here!](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/batch-analysis?view=doc-intel-4.0.0/)

## Running the Program

Have the pdfs you want to process in the pdf-api-container blob storage file
Have an output folder for the json txt data
To run the program, locate the file a terminal like powershell and run
`python .\dole_doc_api.py`

## Usage

Once the program is running, don't exit the terminal window or cancel the program until it's finished.

**IT MIGHT TAKE A WHILE!**

## Contact

For any questions or support, please contact [g676s040@ku.edu](mailto:g676s040@ku.edu)
