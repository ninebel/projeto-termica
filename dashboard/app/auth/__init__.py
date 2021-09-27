from flask import Flask, render_template, redirect, url_for, request, session, flash, Blueprint, jsonify
from functools import wraps
import json
import random
from config import *
from app import app, api_call
from app.utils import login_required, guest_required
from .forms import Login
import datetime

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates', static_folder='static', url_prefix='/auth') # Blueprint object

# ---------------------------------------------------------------
# BLUEPRINT SETUP
# ---------------------------------------------------------------
@auth_bp.before_app_first_request # This function is executed when the bueprint is registered in the application
def init(): 

    pass


# ---------------------------------------------------------------
# VIEWS (ROUTES)
# ---------------------------------------------------------------    

""" Login """
@auth_bp.route('/login', methods=['POST' , 'GET'])
@guest_required
def login():

    formLogin = Login()

    if request.method == 'POST' and formLogin.validate():
        
        if formLogin.password.data == '1234': # If the user email exists, so he's registered    
                                
            # Log-in the user and open a session
            session.pop('_flashes', None) # Clear flash messages
            session['id'] = 'my_id'
            session.permanent = False
            app.permanent_session_lifetime = datetime.timedelta(minutes=15)
            # ---------------------
            return redirect(url_for('auth_bp.login'))

        else:
            flash('A senha está incorreta!')

    # Flash the errors with the form
    for field, errors in formLogin.errors.items():
        for error in errors:
            flash(error)

    return render_template('login.html', formLogin=formLogin)


""" Logout """
@auth_bp.route('/logout', methods=['POST' , 'GET'])
@login_required
def logout():
    
    session.pop('id', None)
    return redirect(url_for('auth_bp.login'))