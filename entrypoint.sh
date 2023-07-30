#!/bin/bash

# タイムゾーンを設定
if [ -n "$TZ" ]; then
    ln -snf "/usr/share/zoneinfo/$TZ" /etc/localtime
    echo "$TZ" > /etc/timezone
fi

# cronジョブを設定
echo "0 8 * * * /usr/local/bin/python3 /app/main.py" > /etc/cron.d/crontab
echo "0 0 * * * /usr/local/bin/python3 /app/code_list_batch.py" > /etc/cron.d/crontab

# cronデーモンを起動
cron

# /app/code_list_batch.py を実行
/usr/local/bin/python3 /app/code_list_batch.py

# /app/code_list_batch.py を実行
/usr/local/bin/python3 /app/target_code.py

# コンテナのメインプロセスを実行
exec "$@"