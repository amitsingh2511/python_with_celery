import io
import time
from celery import Celery
# from main_file import process_csv

broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'

# command calery -A calery_worker.calery worker --loglevel=info
# command calery -A calery_worker flower --port=555

calery = Celery(__name__)
calery.conf.broker_url = broker_url
calery.conf.result_backend = result_backend

@calery.task(name="create_task")
def create_task(csv_contents):
    # process_csv(csv_contents)
    return