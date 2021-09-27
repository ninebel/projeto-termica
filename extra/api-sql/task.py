from .app import app, db

celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
celery.conf.timezone = 'UTC' # Redundant, because default is UTC

from .config import ativos
celery.conf.beat_schedule = {
    'run_alerts-1m': {
        'task': 'run_alerts',
        'schedule': 60.0, # 1x60 = 60
        'args': (ativos, '5m', '2d')
    },
}

# ---------------------------------------------------------------
# SCHEDULED TASKS
# ---------------------------------------------------------------

@celery.task
def run_alerts(assets, interval, period):

    return 'OK'