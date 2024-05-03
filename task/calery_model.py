from fastapi import HTTPException
import io
import time
from celery import Celery
from db import Session , Task
import csv
import logging

broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'

# command calery -A calery_worker.calery worker --loglevel=info
# command calery -A calery_worker flower --port=555

calery = Celery(__name__)
calery.conf.broker_url = broker_url
calery.conf.result_backend = result_backend

# @calery.task(name="create_task")
# def create_task(csv_contents):
#     # process_csv(csv_contents)
#     return


@calery.task(name="task")
def process_csv(csv_contents):
    print(".....Amit")
    try:
        lines = csv_contents.decode('iso-8859-1').split('\n')
        print("-----",lines)
        
        session = Session()
        for line in csv.reader(lines):
            
            new_task = Task(task_id=line[0], status=line[1])  
            session.add(new_task)
            
            session.commit()
        
        logging.info("CSV file processing completed and data inserted into the database")

    except Exception as e:
        logging.error("Error occurred while processing CSV: %s", e)
        raise HTTPException(status_code=500, detail="Failed to process CSV")
