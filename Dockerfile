FROM python:3.10-slim-buster
WORKDIR /gru
COPY requirements.txt /gru/
RUN pip install -r requirements.txt
COPY . /gru
CMD python main.py
