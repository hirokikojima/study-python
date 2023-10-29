FROM python:3.12

WORKDIR /app

RUN apt-get update
RUN pip install --upgrade pip

COPY ./src .

CMD [ "python", "app.py" ]