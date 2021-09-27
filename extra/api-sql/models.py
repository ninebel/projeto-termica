from .app import *
from .app import db

class Furnace(db.Model):

    __tablename__ = 'furnace'

    id = db.Column(db.Integer, primary_key=True, nullable=False, index=True) # Unique ID for each alert
    running = db.Column(db.Boolean, nullable=False) # If the alert is enabled or not
    name = db.Column(db.String(50), nullable=False) # Alert name (for user control)
    zone = db.Column(db.String(50), nullable=False) # Alert name (for user control)


class FurnaceData(Furnace):

    __tablename__ = 'furnace_data'

    id = db.Column(db.Integer, primary_key=True, nullable=False, index=True)
    temperature = db.Column(db.Float(), nullable=False) # Temperature is float
    humidity = db.Column(db.Float(), nullable=False) # Humidity is float
    #vibration = db.Column(db.Float(), nullable=False) # Vibration is float
    voltage = db.Column(db.Float(), nullable=False) # Voltage is float
    current = db.Column(db.Float(), nullable=False) # Current is float

