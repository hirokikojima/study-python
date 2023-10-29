FROM python:3.12

WORKDIR /code

RUN apt-get update
RUN pip install --upgrade pip

# パッケージインストール
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r ./requirements.txt

# ソースコードのコピー
COPY ./app /code/app

EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]