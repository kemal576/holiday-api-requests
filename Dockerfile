FROM python:3.10

COPY ./src /app/src
COPY ./tests /app/tests
COPY ./requirements.txt /app

WORKDIR /app

RUN pip3 install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app"

CMD ["python", "src/main.py"]