FROM python:3.8-slim
COPY . app/
RUN pip install -r app/requirements.txt
CMD ["python", "app/main.py"]