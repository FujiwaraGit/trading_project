# 公式のPython 3.14イメージをベースに使用
FROM python:3.11.4

# コンテナ内の作業ディレクトリを/appに設定
WORKDIR /app

# requirements.txtファイルを現在のディレクトリからコンテナの/appディレクトリにコピー
COPY requirements.txt .

# pipを最新バージョンにアップグレード
RUN pip install --upgrade pip

# requirements.txtに記載されたPythonの依存パッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

#pycong2を別途インストール
RUN pip install psycopg2

# PostgreSQLクライアントとlibpq-devをインストール
RUN apt-get update \
    && apt-get install -y postgresql-client libpq-dev
