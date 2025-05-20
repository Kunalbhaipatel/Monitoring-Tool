
from fastapi import FastAPI, UploadFile, File
import pandas as pd
from influxdb_client import InfluxDBClient, Point, WriteOptions

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "API running"}

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    df['Timestamp'] = pd.to_datetime(df['YYYY/MM/DD'] + ' ' + df['HH:MM:SS'], errors='coerce')
    df['SHAKER Output'] = df.get('SHAKER #1 (Units)', 0).fillna(0) + df.get('SHAKER #2 (Units)', 0).fillna(0)

    client = InfluxDBClient(
        url="https://us-east-1-1.aws.cloud2.influxdata.com",
        token="your-influx-token",
        org="derrick"
    )
    write_api = client.write_api(write_options=WriteOptions(batch_size=500))

    for row in df.itertuples():
        if pd.isna(row.Timestamp): continue
        point = (
            Point("shaker")
            .tag("rig", "Rig1")
            .field("shaker_output", float(row._asdict().get("SHAKER Output", 0)))
            .time(row.Timestamp)
        )
        write_api.write(bucket="shaker_data", record=point)

    return {"rows": len(df), "status": "uploaded"}
