import paho.mqtt.client as MQTT
import time
import json
from datetime import datetime
from pymongo import MongoClient, collection
from config import *

""" Upload data to MongoDB """
def create_document(message):

    json_message = json.loads(message)
    db = json_message['db'] # Get the DB name
    collection = json_message['collection'] # Get the collection name
    data = json_message['data'] # Get the data to be inserted
    db_client[db][collection].insert_one( data ) # Insert data in Python Dictionary type!!
    print('MQTT Listener > Dados gravados no MongoDB')


""" MQTT Callback - called when client connected to broker """
def on_connect(client, userdata, flags, rc):
    print('MQTT Listener > Conectado ao broker')


""" MQTT Callback - called when a message is received on your subscribed channel """
def on_message(client, userdata, msg):
    message = msg.payload.decode('utf-8')
    print('MQTT Listener > Dados recebidos:', msg.topic + "=" + message)
    create_document(message)


""" MQTT Callback - called when a message is published """
def on_publish(client, userdata, result):             
    print('MQTT Listener > Dados publicados')


""" MQTT Callback - called when a client disconnected from broker """
def on_disconnect(client, userdata, rc=0):
    print('MQTT Listener > Desconectado do broker')
    client.loop_stop()


""" MongoDB Configuration """
def config_db():
    while True:
        try:
            db_client = MongoClient(MONGO_CONNECTION_STRING)
            print('MQTT Listener > Database configurada')
            return db_client
        except Exception as e:
            print('MQTT Listener > Falha ao configurar database')
            print(e)
            print('MQTT Listener > Tentando novamente em 5 segundos...')
            time.sleep(5)


""" MQTT Configuration """
def config_mqtt():
    while True:
        try:
            mqtt_client = MQTT.Client(MQTT_CLIENT)
            # Callbacks
            mqtt_client.on_connect = on_connect
            mqtt_client.on_message = on_message
            mqtt_client.on_publish = on_publish
            mqtt_client.on_disconnect = on_disconnect
            mqtt_client.connect(MQTT_BROKER)
            mqtt_client.subscribe(MQTT_CHANNEL_VARIABLES)
            print('MQTT Listener > mqtt configurado')
            return mqtt_client
        except Exception as e:
            print('MQTT Listener > Falha ao configurar mqtt')
            print(e)
            print('MQTT Listener > Tentando novamente em 5 segundos...')
            time.sleep(5)


""" MAIN LOGIC """
db_client = config_db() # MongoDB
mqtt_client = config_mqtt() # MQTT

# Infinite loop
while True:
    try:
        mqtt_client.loop_start()
        time.sleep(120)
        mqtt_client.loop_stop()
    except Exception as e:
        print('MQTT Listener > Erro fatal')
        print(e)
        time.sleep(0.5)