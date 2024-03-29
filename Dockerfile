FROM python:3.11

COPY requirements.txt /tmp/

RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY src /app

COPY api_key.txt /app/api_key.txt
ENV PYTHONPATH=/app

ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

ENTRYPOINT  ["bash", "./start.sh"]
