from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.documentintelligence.models import AnalyzeBatchDocumentsRequest, AzureBlobContentSource
from azure.ai.documentintelligence.aio import DocumentIntelligenceClient
from azure.storage.blob.aio import ContainerClient

async def analyze_batch_docs(pdf_api_container, pdf_output_container, api_key, endpoint):
    continue_to_extract = 0
    #create async DocumentIntelligenceClient
    async with DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(api_key)) as document_intelligence_client:
        request = AnalyzeBatchDocumentsRequest(
            result_container_url=pdf_output_container,
            azure_blob_source=AzureBlobContentSource(
                container_url=pdf_api_container,
            ),
        )
        poller = await document_intelligence_client.begin_analyze_batch_documents(
            model_id="prebuilt-layout",
            body=request,
        )
        #wait until the batch analysis is complete
        print("Analyzing batch documents. Don't close this window...")
        final_result = await poller.result()
        continue_to_extract = final_result.succeeded_count
        if continue_to_extract > 0: print(f"Succeeded count: {continue_to_extract}")
        if final_result.failed_count > 0: print(f"Failed count: {final_result.failed_count}")
        if final_result.skipped_count: print(f"Skipped count: {final_result.skipped_count}")
    if continue_to_extract > 0: #delete blobs from the pdf_api_container after successful scanning
        print("Deleting blobs from the pdf_api_container...")
        container_client = ContainerClient.from_container_url(pdf_api_container)
        count = 0
        async with container_client:
            async for blob in container_client.list_blobs():
                await container_client.delete_blob(blob.name)
                count += 1
        print(f"Deleted {count} blobs from the pdf_api_container")
        print("Batch document analysis complete!")
    return continue_to_extract

async def batch(config, config_path):
    continue_to_extract = 0
    try:
        #read configuration from env.ini
        config.read(config_path)
        pdf_api_container = config.get('DocumentAI', 'pdf_api_container')
        pdf_output_container = config.get('DocumentAI', 'pdf_output_container')
        api_key = config.get('DocumentAI', 'api_key')
        endpoint = config.get('DocumentAI', 'endpoint')
        continue_to_extract = await analyze_batch_docs(pdf_api_container, pdf_output_container, api_key, endpoint)
    except HttpResponseError as error:
        if error.error is not None:
            if error.error.code == "InvalidImage":
                print(f"Received an invalid image error: {error.error}")
            if error.error.code == "InvalidRequest":
                print(f"Received an invalid request error: {error.error}")
            raise
        if "Invalid request".casefold() in error.message.casefold():
            print(f"Uh-oh! Seems there was an invalid request: {error}")
        raise
    return continue_to_extract