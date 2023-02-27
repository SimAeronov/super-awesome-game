FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD gunicorn --bind 0.0.0.0:5000 wsgi:app
# gunicorn -b 0.0.0.0:5000 --workers 4 --threads 100 module:app