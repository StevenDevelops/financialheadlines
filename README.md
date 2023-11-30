# Financial Headlines
A Python script to get financial headlines from NASDAQ feed

## Setting up your environment

* You first want to create a Storage Account, with a Container in Azure
* At the project root, create an `.env` file with the following variables
```text
BLOB_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName ...rest of your Storage connection string in quotes"
BLOB_CONTAINER_NAME=yourcontainername
```
* From your Storage account, paste your blob storage connection string, and blob storage container name into the `.env`
file

## How to run script
Specify one ticker symbol, such as `MSFT` as an argument. The script will pull the feed based on the ticker symbol
you provide. The script has no support for more than 1 symbol.
```commandline
python3 main.py MSFT
```
