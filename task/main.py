# main.py

import logging
import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from celery import Celery
# from celeryconfig import celery
from calery_model import create_task
import csv

# FastAPI setup
app = FastAPI()

from celery import Celery

broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'


celery = Celery(__name__)
celery.conf.broker_url = broker_url
celery.conf.result_backend = result_backend


# SQLAlchemy setup
DB_URI = "postgresql://postgres:8969037429@localhost:5432/testdb"
engine = create_engine(DB_URI)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Define model for database table
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    task_id = Column(String)
    status = Column(String)


# Celery task to process each row in the CSV file
@celery.task(name="task")
def process_csv(csv_contents):
    print(".....")
    logging.info("Processing CSV file contents")
    try:
        # Split the CSV contents into lines
        lines = csv_contents.decode().split('\n')
        
        session = Session()
        # Process each line of the CSV file
        for line in csv.reader(lines):
            # Insert data into the database
            new_task = Task(task_id=line[0], status=line[1])  # Assuming task_id and status are in columns 0 and 1
            session.add(new_task)
            
            # Commit the transaction after inserting each row into the database
            session.commit()
        
        logging.info("CSV file processing completed and data inserted into the database")

    except Exception as e:
        # Log any exceptions that occur during data insertion
        logging.error("Error occurred while processing CSV: %s", e)
        raise HTTPException(status_code=500, detail="Failed to process CSV")
    
    
# FastAPI endpoint to accept CSV file and trigger processing
@app.post("/process-csv/")
async def process_csv_file(file: UploadFile = File(...)):
    # Read the contents of the uploaded CSV file from memory
    csv_contents = await file.read()

    # Trigger Celery task to process the CSV file contents asynchronously
    try:
        create_task.delay(csv_contents)
    except Exception as e:
        print("e----",e)

    return {"message": "CSV file processing started"}

if __name__ == "__main__":
    Base.metadata.create_all(engine)
