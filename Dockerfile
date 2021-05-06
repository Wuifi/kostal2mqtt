FROM arm32v7/python:3.8-slim-buster

#FROM python:3.8-slim-buster

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt /
COPY kostal2mqtt.py /
#RUN pip3 install git+https://github.com/rcasula/kostalpiko.git
RUN pip3 install --no-cache-dir -r requirements.txt
CMD [ "python3", "./kostal2mqtt.py" ]


