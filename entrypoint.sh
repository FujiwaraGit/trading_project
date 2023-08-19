#!/bin/bash

# タイムゾーンを設定
if [ -n "$TZ" ]; then
    ln -snf "/usr/share/zoneinfo/$TZ" /etc/localtime
    echo "$TZ" > /etc/timezone
fi

# データベースの起動を待つ処理を追加
while ! nc -z db 5432; do
    echo "Waiting for the database to start..."
    sleep 1
done

# /app/code_list_batch.py を実行
/usr/local/bin/python3 /app/code_list_batch.py

# /app/code_list_batch.py を実行
/usr/local/bin/python3 /app/target_code.py

#スケジューラを起動
/usr/local/bin/python3 /app/scheduler.py

# コンテナのメインプロセスを実行
exec "$@"
