FROM python:3.7-slim

RUN mkdir /app

WORKDIR /app

RUN pip install requests

COPY ./src .

CMD ["python", "main.py"]