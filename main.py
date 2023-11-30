# Import statements
import requests
import xml.etree.ElementTree as ElementTree
import json
from azure.storage.blob import ContainerClient, ContentSettings
from dotenv import load_dotenv
import os


# Load environment variables
# TO DO: Want to print these env variables
# Throw some errors when required varibles aren't set
# Make the script take in Ticker Symbols as parameter
# Create a README on how to run
load_dotenv()
blob_connection_string = os.getenv("BLOB_CONNECTION_STRING")
container_name = os.getenv("BLOB_CONTAINER_NAME")


def fetch_headlines(ticker_symbol):
    # Prepare the URL to make a request
    url = "https://www.nasdaq.com/feed/rssoutbound?symbol=" + ticker_symbol

    # Set the user agent for the request
    headers = {'User-Agent': 'DurableBank/1.0.0'}

    # Make the request and parse response
    response = requests.get(url, headers=headers)
    return parse_response(response.content)


def parse_response(content):
    root = ElementTree.fromstring(content)

    # Store all json in this resulting list
    full_payload = []

    # Parse through each Node in the XML document
    for node in root.iter('item'):
        headline = node.find('title').text
        timestamp = node.find('pubDate').text
        datasource = node.find('link').text
        description = node.find('description').text.strip()

        # If description is still empty, no parse happened...
        # It's in paragraph format, so extract text this way
        if description == "":
            for paragraph in root.iter('p'):
                description += " " + paragraph.text.strip()
                for anchor in root.iter('a'):
                    description += " " + anchor.text.strip()

        # Use the XML namespace to find the ticker symbols
        namespaces = {'nasdaq': 'http://nasdaq.com/reference/feeds/1.0'}
        symbols = node.find('nasdaq:tickers', namespaces).text.split(',')

        # Only include unique symbols
        symbols = list(set(symbols))

        # Dictionary to represent each JSON payload
        payload = {
            "headline": headline,
            "timestamp": timestamp,
            "datasource": datasource,
            "description": description,
            "symbols": symbols
        }

        full_payload.append(payload)

    # A list of dictionaries representing json payload
    return full_payload


def push_headlines_to_container(json_list):
    # Connect to storageContainer Client
    container_client = ContainerClient.from_connection_string(
        blob_connection_string,
        container_name=container_name,
    )

    # Create a set of unique blob names
    unique_blobs = set()
    blobs = container_client.list_blobs()
    for blob in blobs:
        unique_blobs.add(blob.name)

    my_content_settings = ContentSettings(content_type='application/json')

    # Push each blob to container if it doesn't exist in container
    for json_dict in json_list:
        # Get the headline URL
        headline_url = json_dict['datasource']

        # Convert the headline URL into a hash (unique identifier)
        hashed_url = str(abs(hash(headline_url)))
        hashed_url_json = hashed_url + ".json"

        # If blob already exists in Container, skip it
        if hashed_url_json in unique_blobs:
            continue

        # Create metadata for each blob
        metadata = {
            "timestamp": json_dict['timestamp'],
            "symbols": ','.join(json_dict['symbols']),
            "id": hashed_url
        }

        # Upload blobs that aren't already in Container
        data = json.dumps(json_dict, indent=1)
        container_client.upload_blob(
            name=hashed_url_json,
            data=data,
            metadata=metadata,
            content_settings=my_content_settings,
            overwrite=False
        )


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    headlines = fetch_headlines('MSFT')
    push_headlines_to_container(headlines)
