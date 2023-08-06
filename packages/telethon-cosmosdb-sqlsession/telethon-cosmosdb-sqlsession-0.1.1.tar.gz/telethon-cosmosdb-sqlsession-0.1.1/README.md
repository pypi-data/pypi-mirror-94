# Telethon Cosmos DB SQL API Sesion

This is a [Telethon](https://telethon.dev) session backend which uses Cosmos DB (SQL API).

In short, it allows Telethon to store session in Cosmos DB via SQL API.


## Installing
```
pip3 install telethon-cosmosdb-sqlsession
```

## Upgrading
```
pip3 install -U telethon-cosmosdb-sqlsession
```

## Usage
```
from telethon import TelegramClient
from telethoncosmosdb import CosmosDBSQLSession

api_id = 123456
api_hash = "0123456789abcdef0123456789abcdef"
COSMOS_ENDPOINT = 'https://database-endpoint.documents.azure.com:443/'
COSMOS_KEY = 'Cosmos DB key here=='
COSMOS_DBNAME = 'database'

# The first parameter 'user' means the session will create containers with suffix 
# '_user' in the names to avoid any possible name collision (What would happen will happen).
session = CosmosDBSQLSession('user', COSMOS_ENDPOINT, COSMOS_KEY, COSMOS_DBNAME)
client = TelegramClient(session, api_id, api_hash)
```


## Disclaimer

This packages assumes your data is well-encrypted in Cosmos DB, and therefore does not encrypt your session data.

This package comes with no warranty. I am not responsible for any damages resulted from using this package.
