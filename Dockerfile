FROM python:3.9-slim

RUN apt-get update && apt-get install -y make

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["make", "run"]
