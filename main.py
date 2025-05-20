from fastapi import FastAPI, UploadFile, File
import pandas as pd
from influxdb_client import InfluxDBClient, Point, WriteOptions

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "running"}