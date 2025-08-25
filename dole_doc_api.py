import os
import asyncio
import configparser
from analyze_batch import batch
from extract_json import extract

async def main():
    #create and read the configuration
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    #call batch() and check the result
    succeeded_count = await batch(config, config_path)
    if succeeded_count > 0: #if batch succeeded with more than 0, extract JSON content
        await extract(config, config_path)
    else: print("No documents to extract.")

if __name__ == '__main__':
    asyncio.run(main())