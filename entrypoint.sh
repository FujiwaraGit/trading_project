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

# /src/entry_points/set_target_code_entry.py を実行
/usr/local/bin/python3 /src/entry_points/set_target_code_entry.py

# /src/set_code_list_entry.py.py を実行
/usr/local/bin/python3 /src/entry_points/set_code_list_entry.py

# コンテナのメインプロセスを実行
exec "$@"
