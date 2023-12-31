# 公式のPython 3.14イメージをベースに使用
FROM python:3.11.4

# コンテナ内の作業ディレクトリを/srcに設定
WORKDIR /src

# PostgreSQLクライアントとlibpq-devをインストール
RUN apt-get update \
    && apt-get install -y vim \
    && apt-get install -y netcat-openbsd \
    && apt-get install -y postgresql-client libpq-dev

# requirements.txtファイルを現在のディレクトリからコンテナの/srcディレクトリにコピー
COPY requirements.txt .

# pipを最新バージョンにアップグレード
RUN pip install --upgrade pip

# requirements.txtに記載されたPythonの依存パッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

#pycong2を別途インストール
RUN pip install psycopg2

# タイムゾーンを設定
ENV TZ=Asia/Tokyo

# コマンドを実行するエントリーポイントスクリプトを追加
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# コンテナの実行時にエントリーポイントスクリプトを実行
ENTRYPOINT ["/entrypoint.sh"]
