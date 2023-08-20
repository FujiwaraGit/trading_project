# -*- coding: utf-8 -*-
"""
スケジューラを使用して定期的なバッチ処理を実行するスクリプト

このスクリプトは、scheduleライブラリを使用して指定された時刻にバッチ処理スクリプトを実行します。
ita_insert_batch.pyとcode_list_batch.pyというバッチ処理スクリプトを、それぞれ朝8時と毎日0時に実行する設定が含まれています。
"""

# %%
import time
import subprocess
import schedule


def ita_insert_batch_py():
    """
    ita_insert_batch.py を実行する関数
    """
    subprocess.run(["/usr/local/bin/python3", "/app/ita_insert_batch.py"])


def run_code_list_batch_py():
    """
    code_list_batch.py を実行する関数
    """
    subprocess.run(["/usr/local/bin/python3", "/app/code_list_batch.py"])


def main():
    """
    スケジューラを起動するメイン関数
    """
    # 朝8時に ita_insert_batch.py を実行するスケジュールを設定
    schedule.every().day.at("08:00").do(ita_insert_batch_py)

    # 毎日0時に code_list_batch.py を実行するスケジュールを設定
    schedule.every().day.at("00:00").do(run_code_list_batch_py)

    print("スケジューラを起動します")
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
