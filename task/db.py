import logging
import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import csv


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

# database table
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    task_id = Column(String)
    status = Column(String)