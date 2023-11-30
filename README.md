# Financial Headlines
A Python script to get financial headlines from NASDAQ feed

## Setting up your environment

* You first want to create a Storage Account, with a Container in Azure
* At the project root, create an `.env` file with the following variables
```text
BLOB_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName ...rest of your Storage connection string in quotes"
BLOB_CONTAINER_NAME=yourcontainername
```


