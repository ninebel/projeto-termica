import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import datetime
import os
import random

HOST = "https://furnace.documents.azure.com:443/" # Can be found in keys as URL
MASTER_KEY = "3ZTdt8WFJr6qLoeYXrcbrlYKmnpCPCS85SUvriKrlZWwSFGUEPcBVAwJYOfkpAGaEWnWsjHQFKQq2avtU8r5Fg==" # Primary Key
DATABASE_ID = "Furnace"
CONTAINER_ID = "info"

def info_scheme (id, name, zone):

     return {'id':id, 'name':name, 'zone':zone}

def add_forno(id, name, zone):

    container = db.get_container_client(CONTAINER_ID)
    container.create_item(body=info_scheme(id , name, zone))

client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY} )
db = client.get_database_client(DATABASE_ID)
add_forno('1', 'forno1', 'Zona A')
