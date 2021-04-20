FROM python:3.8-slim

COPY requirements.txt /
COPY kostal2mqtt.py /

RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "./kostal2mqtt.py" ]
