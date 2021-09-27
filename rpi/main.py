from logging import raiseExceptions
from pycomm3 import LogixDriver
import paho.mqtt.client as MQTT
import json
import time
import datetime
from config import *


""" Read variable from PLC """
def read_variable(variable):

    with LogixDriver(PLC_IP) as plc:

        response = plc.read(variable)

        if response[3] == None:

            value = response[1]

            if variable == 'TT1':

                # Line Equation for converting decimal to temperature (f(x) = A*x + B)
                A = (T2 - T1) / (D2 - D1)
                B = T2 - D2*((T2-T1)/(D2-D1))
                value = A*value + B # Convert value to temperature

            elif variable == 'TT2':

                # Line Equation for converting decimal to temperature (f(x) = A*x + B)
                A = (T2 - T1) / (D2 - D1)
                B = T2 - D2*((T2-T1)/(D2-D1))
                value = A*value + B # Convert value to temperature

            return round(value, 2)

        else:
            raise Exception(response[3])


""" Write variable to PLC """
def write_variable(variable, value):

    with LogixDriver(PLC_IP) as plc:

        response = plc.write(variable , value)

        if response[3] == None:
            return response[1] # Returns the value in the variable...
        
        else:
            raise Exception(response[3])


""" Send data to MQTT broker """
def publish_data (variable, value):

    message = { 'db':DB , 'collection':variable , 'data':{ 'time':datetime.datetime.now().strftime('%d/%B/%Y %H:%M:%S')  , 'value':value }  } # Message body in JSON format
    mqtt_client.publish( MQTT_CHANNEL_VARIABLES , json.dumps(message) ) # Publish the message


""" MQTT Callback - called when client connected to broker """
def on_connect(client, userdata, flags, rc):
    print('Raspberry Pi > Conectado ao broker')


""" MQTT Callback - called when a message is received on your subscribed channel """
def on_message(client, userdata, msg):

    topic = msg.topic
    message = msg.payload.decode('utf-8')
    json_message = json.loads(message)
    
    print('Raspberry Pi > Received:', topic, '=', message)

    # Commands
    if topic == MQTT_CHANNEL_COMMANDS:

        try:
            
            if json_message['command'] == 'read':

                publish_data( json_message['variable'], read_variable(json_message['variable']) )

            elif json_message['command'] == 'write':

                write_variable( json_message['variable'] , value=json_message['value'] )

        except Exception as e:
            print('Raspberry Pi > Erro ao executar comando', e)


""" MQTT Callback - called when a message is published """
def on_publish(client, userdata, result):             
    print('Raspberry Pi > Dados publicados')


""" MQTT Callback - called when a client disconnected from broker """
def on_disconnect(client, userdata, rc=0):
    print('Raspberry Pi > Desconectado do broker')
    client.loop_stop()


""" MQTT Configuration """
def config_mqtt():
    while True:
        try:
            mqtt_client = MQTT.Client(MQTT_CLIENT)
            mqtt_client.on_connect = on_connect
            mqtt_client.on_message = on_message
            mqtt_client.on_publish = on_publish
            mqtt_client.on_disconnect = on_disconnect
            mqtt_client.connect(MQTT_BROKER)
            mqtt_client.subscribe(MQTT_CHANNEL_COMMANDS)
            print('Raspberry Pi > MQTT Configurado')
            return mqtt_client

        except Exception as e:
            print('Raspberry Pi > Falha ao configurar MQTT')
            print(e)
            print('Raspberry Pi > Tentando novamente em 5 segundos...')
            time.sleep(5)


""" MAIN LOGIC """
mqtt_client = config_mqtt() # MQTT config

# Set the start time for each var.
startTime = {}
lastValue = {}
for variable in READ_VARIABLES:
    startTime[variable] = time.perf_counter()
    lastValue[variable] = 0.001
# ------------------------------------

# Infinite Loop for reading variables
while True:

    try:

        mqtt_client.loop_start() # Start MQTT loop, this takes care of automatically receiving/writting messages

        # Read variable for each key in READ_VARIABLES
        for variable in READ_VARIABLES:

            deltaTime = time.perf_counter() - startTime[variable]

            if deltaTime >= READ_VARIABLES[variable]:

                startTime[variable] = time.perf_counter()
                value = read_variable(variable)

                try:
                    change = value/lastValue[variable] # value/lastValue -> change

                except ZeroDivisionError:
                    change = 1

                if change >= (1 + MINIMUM_CHANGE/100) or change <= (1 - MINIMUM_CHANGE/100): # If there was a minimum change...

                    publish_data( variable, read_variable(variable) )
                    lastValue[variable] = value # Update last inserted value...
        # ------------------------------------

        mqtt_client.loop_stop() # End MQTT loop

    except Exception as e:

        print('Raspberry Pi > Erro fatal ao ler as variáveis', e)
        time.sleep(0.5)
# ------------------------------------

