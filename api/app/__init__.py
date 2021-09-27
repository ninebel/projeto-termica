from flask import Flask, render_template, redirect, url_for, request, session, flash, Blueprint, jsonify
from functools import wraps
from datetime import datetime
import os
import json
import paho.mqtt.client as mqtt
import random
from pymongo import MongoClient, collection
from config import *

# App
app = Flask(__name__) # Create app instance/object
app.config.from_object('config') # App config

# MongoDB
client = MongoClient(CONNECTION_STRING)
db = ''
collection = ''

# ---------------------------------------------------------------
# API AUTHENTICATION
# ---------------------------------------------------------------

""" This function is executed when an endpoint is called """
@app.before_request
def before_request():

    global db
    global collection
    try:
        db = client[ request.json['db'] ] # Select DB      
        collection = db[ request.json['collection'] ] # Select collection
    except:
        # In case the container selection fails, the request ends here
        return jsonify({ 'status':'error', 'error':'db/collection was not specified in request' })



# ---------------------------------------------------------------
# API ENDPOINTS
# ---------------------------------------------------------------

""" 
READ ITEMS/DOCUMENTS
Example usage: requests.get('http://link:port/read', json={'db':'Forno_PUCPR','collection':'TT1','data':{'value':100} })
"""
@app.route('/read', methods=['GET'])
def read_items():

    try:
        filter = request.json['data']
        cursor = collection.find(filter)
        items = []
        for item in cursor:
            item['_id'] = str(item['_id']) # This transforms the ObjectId and fixes a JSON serialization error!
            items.append(item)
        return jsonify({ 'status':'ok' , 'result':items })

    except Exception as e:
        return jsonify({ 'status':'error', 'error':str(e) })


"""
CREATE AN ITEM/DOCUMENT
Example usage: requests.post('http://link:port/create', json={'db':'Forno_PUCPR','collection':'TT1','data':{'time':'2021-04-16 01:38:29.868610' , 'value':100} })
"""
@app.route('/create', methods=['POST'])
def create_item():

    try:
        data = json.loads(request.json['data'])
        collection.insert_one( data ) # Insert data in Python Dictionary type!!

        return jsonify({ 'status':'ok' })

    except Exception as e:
        return jsonify({ 'status':'error', 'error':str(e) })

"""
DELETE ITEM/DOCUMENT FROM CONTAINER
Example usage: requests.get('http://link:port/delete', json={'db':'Forno_PUCPR','collection':'TT1','data':{'value':100} })
"""
@app.route('/delete', methods=['POST'])
def delete_items():

    try:
        filter = json.loads(request.json['data'])
        result = collection.delete_many(filter)
        print(result)

        return jsonify({ 'status':'ok' })

    except Exception as e:

        return jsonify({ 'status':'error', 'error':str(e) })

"""
SPECIFIC COMMANDS 
Example usage: requests.get( 'http://link:port/command', json={'db':'Forno_PUCPR','collection':'TT1','data':{'command':'read', 'variable':'TT1'}} )
"""
@app.route('/command', methods=['POST'])
def command():

    try:

        mqtt_client = mqtt.Client(str(random.randint(0, 10000))) # Client's name is random so we avoid client naming conflicts in case of multithreading!
        mqtt_client.connect(MQTT_BROKER)

        # For a command to be executed, it needs to be sent to Raspberry Pi via MQTT protocol
        command = request.json['data']['command']
        variable = request.json['data']['variable']

        if command.lower() == 'read':

            message = {'command':command , 'variable':variable} # Time and value received from PLC
            mqtt_client.publish( MQTT_CHANNEL_COMMANDS, json.dumps(message) ) # Publish the message          

        elif command.lower() == 'write':

            value = request.json['data']['value']
            message = {'command':command , 'variable':variable, 'value':value} # Time and value received from PLC
            mqtt_client.publish( MQTT_CHANNEL_COMMANDS, json.dumps(message) ) # Publish the message   

        return jsonify({ 'status':'ok' })

    except Exception as e:

        return jsonify({ 'status':'error', 'error':str(e) })
