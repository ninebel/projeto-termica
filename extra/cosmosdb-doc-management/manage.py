import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
from config import *

# Reference: https://github.com/Azure/azure-sdk-for-python/blob/master/sdk/cosmos/azure-cosmos/samples/document_management.py

def query_items(container, doc_id):
    print('\n1.4 Querying for an  Item by Id\n')

    # enable_cross_partition_query should be set to True as the container is partitioned
    items = list(container.query_items(
        query="SELECT * FROM r WHERE r.furnace=@furnace",
        parameters=[
            { "name":"@furnace", "value": doc_id }
        ],
        enable_cross_partition_query=True
    ))

    print('Item queried by Id {0}'.format(items[0].get("id")))

def delete_item(container, doc_id, part_key):
    print('\n1.7 Deleting Item by Id\n')

    response = container.delete_item(item=doc_id, partition_key=part_key)

    print('Deleted item\'s Id is {0}'.format(doc_id))

def delete_all_items(container, partition_key):

    # QUERY ALL ITEMS IN A CONTAINER WITH A COMMON PARTITION KEY
    # enable_cross_partition_query should be set to True as the container is partitioned
    items = list(container.query_items(
        query="SELECT * FROM c",
        enable_cross_partition_query=True
    ))

    # DELETE ALL QUERIED ITEMS
    for i in range (len(items)):
        id = items[i]['id']
        print(id)
        print(type(id))
        delete_item(container, id, id)


client = cosmos_client.CosmosClient(HOST, {'masterKey': PRIMARY_KEY} )
db = client.get_database_client('Furnaces')
container = db.get_container_client('Forno PUCPR')
delete_all_items(container, 'Forno PUCPR')