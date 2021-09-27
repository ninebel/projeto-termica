from flask import Flask, render_template, redirect, url_for, request, session, flash, Blueprint, jsonify
from functools import wraps
import json
import random
from config import *
from app import api_call
from app.utils import login_required
from .forms import ReadPLCVariable, WritePLCVariable

control_bp = Blueprint('control_bp', __name__, template_folder='templates', static_folder='static', url_prefix='/control') # Blueprint object

# ---------------------------------------------------------------
# BLUEPRINT SETUP
# ---------------------------------------------------------------
@control_bp.before_app_first_request # This function is executed when the bueprint is registered in the application
def init(): 

    pass


# ---------------------------------------------------------------
# VIEWS (ROUTES)
# ---------------------------------------------------------------    

@control_bp.route('/', methods=['POST' , 'GET'])
@login_required
def index():

    formReadVar = ReadPLCVariable()
    formWriteVar = WritePLCVariable()
    response = ''

    try:

        if request.method == 'POST':

            if formReadVar.validate_on_submit() and formReadVar.__class__.__name__ in request.form.keys():
                
                response = api_call('command', data= {'db':'Forno_PUCPR','collection':'TT1','data':{'command':'read', 'variable':formReadVar.variable.data }} )

            if formWriteVar.validate_on_submit() and formWriteVar.__class__.__name__ in request.form.keys():

                # Value convertion
                if formWriteVar.type.data == 'text':

                    value = str(formWriteVar.value.data)

                elif formWriteVar.type.data == 'numeric':

                    value = float(formWriteVar.value.data)

                response = api_call('command', data= {'db':'Forno_PUCPR','collection':'TT1','data':{'command':'write', 'variable':formWriteVar.variable.data, 'value':value }} )

            if response == 'ok':
                flash('Comando enviado!')
            else:
                flash(response)

            #return redirect(url_for('control_bp.index')) # Redirects to the same page, so the fields are cleaned 

    except Exception as e:

        flash(e)

    #formReadVar = ReadPLCVariable()
    #formWriteVar = WritePLCVariable()

    return render_template('control.html', page='control', formReadVar=formReadVar, formWriteVar=formWriteVar)
