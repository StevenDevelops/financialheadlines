# Financial Headlines
A Python script to get financial headlines from NASDAQ feed, and pushes those headlines to your Azure container. 
Each headline in your container would look like this
```json
{
 "headline": "Could Investing in the Nasdaq-100 Help You Retire a Millionaire?",
 "timestamp": "Thu, 30 Nov 2023 12:15:00 +0000",
 "datasource": "https://www.nasdaq.com/articles/could-investing-in-the-nasdaq-100-help-you-retire-a-millionaire",
 "description": "While some may consider index fund investing boring, there is no easier way to put yourself on a path to success than consistently adding to an index fund. In fact, I'd argue that many investors would be better suited to doing this than buying individual stocks they don't have th",
 "symbols": [
  "GOOG",
  "AAPL",
 ]
}
```

## Setting up your environment

* You first want to create a Storage Account, with a Container in Azure
* At the project root, create an `.env` file with the following variables
```text
BLOB_CONNECTION_STRING="storage connection string in quotes"
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
