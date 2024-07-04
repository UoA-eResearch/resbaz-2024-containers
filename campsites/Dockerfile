FROM python:3.12.4-alpine3.20

WORKDIR /app

ADD requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ADD . .

CMD ["python", "tally.py"]
