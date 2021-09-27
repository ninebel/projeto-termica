from flask import Flask, render_template, redirect, url_for, request, session, flash, Blueprint, jsonify
from functools import wraps
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
from config import *
from app import api_call
from app.utils import login_required
from .forms import ReadData

data_bp = Blueprint('data_bp', __name__, template_folder='templates', static_folder='static', url_prefix='/data') # Blueprint object

# ---------------------------------------------------------------
# BLUEPRINT SETUP
# ---------------------------------------------------------------
@data_bp.before_app_first_request # This function is executed when the bueprint is registered in the application
def init(): 

    pass


# ---------------------------------------------------------------
# VIEWS (ROUTES)
# ---------------------------------------------------------------    

""" Generate graph for data """
def auto_generate_graph(items, graph_title='', x_title='', y_title=''):

    x = []
    y = []
    for item in items:

        x.append(item['time'])
        y.append(item['value'])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', line_color='rgb(22, 204, 98)', name=''))
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(
        title=graph_title,
        xaxis_title=x_title,
        yaxis_title=y_title,
        xaxis={'gridcolor':'black'},
        yaxis={'gridcolor':'black'},
        legend_title="Legend",
        margin=dict(l=70, r=70, b=70, t=70, pad=10),
        #autosize=True,
        width=1300,
        height=750,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,100)',
        font=dict(family="Raleway, sans-serif", size=15, color="Black")
    )
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json


""" View """
@data_bp.route('/', methods=['POST' , 'GET'])
@login_required
def index():

    try:

        formReadData = ReadData()
        graph = ''
        variable = ''
        items = ''

        if request.method == 'POST':

            if formReadData.validate_on_submit() and formReadData.__class__.__name__ in request.form.keys():
                
                variable = formReadData.variable.data

                items = api_call('read', data={'db':'Forno_PUCPR','collection':variable,'data':{} } )

                graph = auto_generate_graph(items, graph_title=variable, x_title='Tempo', y_title=variable)

                if items == []:
                    flash('Essa variável não existe!')

    except Exception as e:

        flash(e)

    return render_template('data.html', page='data', formReadData=formReadData, variable='', graph=graph, items=items)
