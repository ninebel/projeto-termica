
# ====================================================================================================================================
# PYCOMM3 (PLC LIBRARY)

PLC_IP = '10.151.0.102/0' # PLC ip/rack 0 for not in rack, 1 for in rack

# ====================================================================================================================================

# ====================================================================================================================================
# MQTT

MQTT_BROKER = 'mqtt.eclipseprojects.io' # MQTT broker/server address
MQTT_CLIENT = 'Forno PUCPR' # MQTT Client's name (also used as furnace's unique identifier)
MQTT_CHANNEL_VARIABLES = 'plc_variables' # Name of the channel containing the data from the PLC variables
MQTT_CHANNEL_COMMANDS = 'commands'

# ====================================================================================================================================

# ====================================================================================================================================
# SCRIPT CONFIGURATION

DB = 'Forno_PUCPR' # DB = Furnace name (DB name can not contain spaces!)

# Format: VARIABLE NAME : SAMPLING TIME IN SECONDS
READ_VARIABLES = {'TT1':0.1, 
                  'TT2':0.1,
                  'Setpoint':0.1,
                  'Controlador[0].KP':10,
                  'Controlador[0].KI':10,
                  'Controlador[0].KD':10,
                  'Controlador[0].PV':0.1,
                  'Controlador[0].SP':0.1} 
                  
# Minimum change (in percentage) between samples to upload data to db, this way we can prevent repeated data and keep the db clean
MINIMUM_CHANGE = 5

# Decimal to temperature conversion
# Point 1
T1 = 0 # f(x)
D1 = 3277 # Decimal value for T1 (x)
# Point 1
T2 = 200 # f(x)
D2 = 16383 # Decimal value for T1 (x)

# ====================================================================================================================================