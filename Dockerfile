FROM python:3.10-slim

WORKDIR /app

COPY . .

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip && \
    pip install fastapi uvicorn pandas influxdb-client

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]