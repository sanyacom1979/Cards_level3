FROM python:3.8.9-slim
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . .
RUN pip install -e ./