FROM python:3.8-slim

WORKDIR /app
COPY . /app

COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8091

CMD ["python", "controller.py"]
