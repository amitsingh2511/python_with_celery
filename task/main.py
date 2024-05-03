# main.py

import logging
import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db import Base, engine
from calery_model import  process_csv
import csv

app = FastAPI()


@app.post("/process-csv/")
async def process_csv_file(file: UploadFile = File(...)):
    csv_contents = await file.read()

    try:
        process_csv.delay(csv_contents)
    except Exception as e:
        print("e----",e)

    return {"message": "CSV file processing started"}

if __name__ == "__main__":
    Base.metadata.create_all(engine)
