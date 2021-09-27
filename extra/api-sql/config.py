# ====================================================================================================================================
# APP
SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/' # Key used for encrypting cookies in bytes
# ====================================================================================================================================

# ====================================================================================================================================
# FLASK-SQLALCHEMY

import urllib.parse
params = urllib.parse.quote_plus("DRIVER={SQL Server};Server=tcp:brazil-south.database.windows.net,1433;Database=furnace;Uid=user;Pwd=Xq2EWu8vdBy56qs3;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=" + params
SQLALCHEMY_TRACK_MODIFICATIONS = False
# ====================================================================================================================================

# ====================================================================================================================================
# CELERY - format: message_queue_protocol://:password@hostname:port/db_number
CELERY_BROKER_URL = 'redis://:12345@80.208.230.217:6379/0' # For the Celery broker, in this case Redis
CELERY_RESULT_BACKEND = 'redis://:12345@80.208.230.217:6379/0' # For the Celery result
# ====================================================================================================================================
