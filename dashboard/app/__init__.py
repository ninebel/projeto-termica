from flask import Flask, render_template, redirect, url_for, request, session, flash, Blueprint, jsonify
from functools import wraps
import requests
import json
from config import *

# =======================================================================================================
# API CONNECTION
# =======================================================================================================

def api_call(endpoint, data):

    if endpoint == 'read':
        r = requests.get(api_url + endpoint, json=data)
        return json.loads(r.text)['result']
    else:
        r = requests.post(api_url + endpoint, json=data)
        return json.loads(r.text)['status']



# =======================================================================================================
# APPLICATION SETUP
# =======================================================================================================

# App
app = Flask(__name__) # Create app instance/object
app.config.from_object('config') # App config

# Blueprints
# Dont move the imports from here or there will will be a circular import error
from .home import home_bp
from .data import data_bp
from .control import control_bp
from .auth import auth_bp
app.register_blueprint(home_bp)
app.register_blueprint(data_bp)
app.register_blueprint(control_bp)
app.register_blueprint(auth_bp)


# =======================================================================================================
# VIEWS
# =======================================================================================================

# Page not found (404)
@app.errorhandler(404)
def page_not_found(error):
    
    return "Página não encontrada!", 404

# Internal error (500)
@app.errorhandler(500)
def internal_error(error):
    
    return "Erro interno!", 500