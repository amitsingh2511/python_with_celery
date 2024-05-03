from celery import Celery

broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'


celery = Celery(__name__)
celery.conf.broker_url = broker_url
celery.conf.result_backend = result_backend
# logging.basicConfig(level=logging.INFO)