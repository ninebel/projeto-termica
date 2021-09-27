from flask import Flask, render_template, redirect, url_for, request, session, flash, Blueprint, jsonify
from functools import wraps
import requests
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
from app.utils import login_required
from config import *


home_bp = Blueprint('home_bp', __name__, template_folder='templates', static_folder='static', url_prefix='/') # Blueprint object

# ---------------------------------------------------------------
# BLUEPRINT SETUP
# ---------------------------------------------------------------
@home_bp.before_app_first_request # This function is executed when the bueprint is registered in the application
def init(): 

    pass

# ---------------------------------------------------------------
# VIEWS (ROUTES)
# ---------------------------------------------------------------

@home_bp.route('/')
@home_bp.route('/home')
@login_required
def index():

    return render_template('home.html', page='home')

