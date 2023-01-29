FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

CMD ["python3.9", "main.py", "--config_file", "config/backend-prod.yaml"]
