# Flask API

from . import * # Import all (*) the imports from __init__.py 

app = Flask(__name__) # Creates the Flask application
app.config.from_pyfile('config.py') # App Configuration
db = SQLAlchemy(app)


from .models import Furnace, FurnaceData

# Create all the tables if they do not exist
db.create_all(bind='__all__')

# Test
forno1 = Furnace(name='a', zone='zona Q')
db.session.add(forno1)
db.session.commit()
users = Furnace.query.all()
print(users)

# ---------------------------------------------------------------
# API AUTHENTICATION
# ---------------------------------------------------------------

@app.before_request # This function is executed when an endpoint is called
def init(): 

    # API authentication
    pass


# ---------------------------------------------------------------
# API ENDPOINTS
# ---------------------------------------------------------------

# Example usage: requests.get('http://link:port/api/furnace/query', json={'owner_id':1}) -> Returns a list with the ID of all the furnace owned by user with ID 1
@app.route('/api/query', methods=['GET'])
def query(**filter):

    # json = {''}
    if filter: # If parameter (filter) were given, so its not a request

        return db.session.query(Furnace).filter_by(**filter).all() # Returns an object

    else: # In case it is a request

        try:

            furnace = db.session.query(Furnace).filter_by(**request.json).all()
            
            furnace_id = []
            for alert in furnace:
                alerts_id.append(alert.id)

            return jsonify({'result': alerts_id})

        except Exception as e:
            return jsonify({'status':str(e)})


# Example usage: requests.post('http://link:port/api/alerts/create', json=data) -> Creates a new alert
@app.route('/api/create', methods=['POST'])
def create():

    # json = {'name':'forno1', 'temperature':float , 'humidity':float , 'vibration':float , 'voltage':float, 'current':float}
    try:

        available_furnaces = {'forno1': FurnaceData}

        furnace_name = request.json['name']
        del request.json['name']

        furnace = furnaces[furnace_name](**request.json)
        db.session.add(furnace)
        db.session.commit()
        return jsonify({'status':'OK'})

    except Exception as e:
        return jsonify({'status':str(e)})


# Example usage: requests.post('http://link:port/api/alerts/delete', json={'id':1}) -> Deletes alert with ID 1
@app.route('/api/delete', methods=['POST'])
def delete():

    try:

        furnace = query(**request.json)[0] # [0] for getting the first result (specific user)
        db.session.delete(furnace)
        db.session.commit()
        return jsonify({'status':'OK'})

    except Exception as e:
        return jsonify({'status':str(e)})


# Example usage: requests.post('http://link:port/api/alerts/set', json={'id':1, 'field':'name', 'value':'Main alert'}) -> Changes the name of alert with ID 1 to 'Main alert'
@app.route('/api/set', methods=['POST'])
def set_attr():

    try:

        field = request.json['field']
        value = request.json['value']
        del request.json['field']
        del request.json['value']
        furnace = query(**request.json)[0]
        setattr(furnace, field, value)
        db.session.commit()
        return jsonify({'status':'OK'})

    except Exception as e:
        return jsonify({'status':str(e)})


# Example usage: requests.get('http://link:port/api/alerts/get', json={'id':1, 'field':'name'}) -> Gets the name of alert with ID 1
@app.route('/api/get', methods=['GET'])
def get_attr():

    try:

        field = request.json['field']
        del request.json['field']
        alert = query(**request.json)[0]
        return jsonify({'status':'OK', 'result':getattr(alert, field)})

    except Exception as e:
        return jsonify({'status':str(e)})