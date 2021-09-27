import logging
from app import app

# This is not executed when gunicorn is running the application \/
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80, debug=True)