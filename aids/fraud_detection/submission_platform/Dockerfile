FROM python:3.13-slim

WORKDIR /app
COPY static /app/static
COPY templates /app/templates
COPY requirements.txt /app
COPY app.py /app
COPY fraud_classifier.pkl /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "app.py"]