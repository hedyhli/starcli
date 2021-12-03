FROM python:3.8.3
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install starcli
