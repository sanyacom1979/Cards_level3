FROM python:3.8.9-slim
COPY . .
RUN pip install -r requirements.txt