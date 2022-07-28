# ベースイメージの指定
FROM python:3.8

# apt-getのバージョンを更新し、SQLite3のインストール
RUN apt-get update
RUN apt-get install -y sqlite3
RUN apt-get install -y libsqlite3-dev

# コンテナ上のワーキングディレクトリの指定
WORKDIR /usr/src/

# ディレクトリとファイルのコピー
COPY ./apps /usr/src/apps
COPY ./bnp /usr/src/bnp
COPY ./local.sqlite /usr/src/local.sqlite
COPY ./requirements.txt /usr/src/requirements.txt

# pipのバージョン更新
RUN pip install --upgrade pip

# ライブラリのインストール
RUN pip install -r requirements.txt

# 環境変数
ENV FLASK_APP "apps.app"

# ネットワークポート
EXPOSE 5000

CMD flask run -h 0.0.0.0 -p $PORT   # Heroku
#CMD flask run -h 0.0.0.0           # ローカル

