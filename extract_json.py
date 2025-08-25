import os
import json
from azure.storage.blob.aio import ContainerClient

async def extract_json_data(output_file_path, pdf_output_container):
    #create container client for pdf_output_container
    container_client = ContainerClient.from_container_url(pdf_output_container)
    #process each blob in the container and save "content" from JSON to a separate text file
    async with container_client:
        async for blob in container_client.list_blobs():
            print(f"Processing blob: {blob.name}")
            try:
                downloader = await container_client.download_blob(blob.name)
                data = await downloader.readall()
                json_data = json.loads(data.decode('utf-8'))
                #check if the JSON has status "succeeded" and contains the "content" key
                content_exists = "analyzeResult" in json_data and "content" in json_data["analyzeResult"]
                if json_data.get("status", "").lower() == "succeeded" and content_exists:
                    #extract filename from blob.name (everything before first ".pdf")
                    blob_name = blob.name
                    idx = blob_name.lower().find(".pdf")
                    filename = blob_name[:idx] if idx != -1 else blob_name
                    filename += ".txt"
                    #create the full file path in the output directory
                    file_path = os.path.join(output_file_path, filename)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(json_data["analyzeResult"]["content"])
                    print(f"Saved content to {file_path}")
                else:
                    reason = "missing 'content' key" if not content_exists else f"status: {json_data.get('status')}"
                    print(f"Skipping blob {blob.name} due to {reason}")
                #delete the blob after processing
                await container_client.delete_blob(blob.name)
                print(f"Deleted blob: {blob.name}")
            except Exception as e:
                print(f"Error processing blob {blob.name}: {e}")
                try:
                    await container_client.delete_blob(blob.name)
                    print(f"Deleted blob: {blob.name}")
                except Exception as e:
                    print(f"Error deleting blob {blob.name}: {e}")

    print(f"Extraction complete! Files saved in {output_file_path}")

async def extract(config, config_path):
    #read configuration from env.ini
    config.read(config_path)
    pdf_output_container = config.get('DocumentAI', 'pdf_output_container')
    output_file_path = config.get('DocumentAI', 'output_file_path')
    await extract_json_data(output_file_path, pdf_output_container)