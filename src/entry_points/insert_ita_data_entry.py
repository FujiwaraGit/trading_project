"""
株価データを取得してPostgreSQLデータベースに保存するプログラム

このプログラムは、立花証券のAPIを使用してリアルタイムの株価データを取得し、
取得したデータをPostgreSQLデータベースに保存します。

プログラムの実行には、立花証券のAPIアカウント情報とPostgreSQLの接続情報が必要です。
また、取得したい株価データの銘柄コードリストも指定する必要があります。

プログラムの流れ:
1. 立花証券のAPIにログインし、アカウントのインスタンスを取得します。
2. ログインが成功した場合、PostgreSQLデータベースに接続します。
3. 祝日でない限り、定期的に株価データの取得とデータベースへの保存を行います。
4. 取得したデータはThreadPoolExecutorを使用して並行して処理します。
5. 毎日15時になると最後の1回だけ株価データを取得し、データベースに保存します。
6. プログラムの終了時にPostgreSQLの接続をクローズします。

注意事項:
- プログラム実行前に、環境変数からAPIアカウント情報とPostgreSQL接続情報をセットアップしてください。
- データベースにはあらかじめita_tableというテーブルを作成しておく必要があります。
- データベースの接続情報はdb_params変数で指定します。
- APIアカウント情報はinsert_ita_api.pyで指定します。
- 取得したい株価データの銘柄コードリストはtarget_code.pyで指定します。

実行方法:
コードを実行する前に、環境変数を設定してください。
プログラムの実行はmain関数を呼び出すことで行います。
main関数内で株価データの取得とデータベースへの保存が行われます。

注意:
本プログラムはあくまでサンプルとして提供されるものであり、実際の運用にはさらなる検証や適応が必要です。
API利用の際は利用規約に従って適切にご利用ください。
"""

# %%
import os
import time
import logging
import psycopg2
import requests
import concurrent.futures
from logic.insert_ita_logic import get_target_code_list, login_and_get_account_instance, execute_task
from log.logging_config import configure_logging
from utilities.utility import handle_log, is_today_holiday
from utilities.custom_exceptions import MissingAPIIdError, NoMatchingCodeError


def main():
    """
    メインの処理を実行する関数

    Returns:
        None
    """
    # ログ設定
    log_filename = "/src/log/insert_ita.log"
    logger = configure_logging(log_filename)

    # 開始のログを出力
    handle_log(logger, f"start: {__name__}", logging.INFO)

    # 本日休日なら終了
    if is_today_holiday() is True:
        handle_log(logger, "completion: Closed due to a holiday.", logging.INFO)
        return

    # try:
    #     # PostgreSQLの接続情報を環境変数から取得
    #     db_params = {
    #         "host": os.environ.get("POSTGRES_HOST"),
    #         "database": os.environ.get("POSTGRES_DB"),
    #         "user": os.environ.get("POSTGRES_USER"),
    #         "password": os.environ.get("POSTGRES_PASSWORD"),
    #     }

    #     # ログインを行い、アカウントのインスタンスを作成
    #     account_instance = login_and_get_account_instance()

    #     # コードリストを取得
    #     code_list = get_target_code_list(db_params, os.environ.get("TACHIBANA_USERID"))

    #     # タスク実行の間隔（秒）
    #     interval = 0.1
    #     # 最大の並行タスク数
    #     max_workers = 10

    #     # ThreadPoolExecutorを作成
    #     with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    #         # 15時までのループを開始
    #         while time.localtime().tm_hour < 15:

    #             start_time = time.time()
    #             # execute_tasksを非同期に実行
    #             executor.submit(execute_task, account_instance, code_list, db_params)

    #             # 次のタスクがinterval秒後に開始されるように調整
    #             elapsed_time = time.time() - start_time
    #             time_to_wait = interval - elapsed_time

    #             if time_to_wait > 0:
    #                 time.sleep(time_to_wait)

    #         # 15時になったら最後の1回だけタスクを実行
    #         executor.submit(execute_task, account_instance, code_list, db_params)
    #         # ログを表示
    #         handle_log(logger, "completion: market closure.", logging.INFO)
    #         return
    # # エラーハンドリング
    # except requests.exceptions.Timeout as e:
    #     # リクエストがタイムアウトした場合
    #     handle_log(logger, f"Request timed out: {e}")
    # except requests.exceptions.ConnectionError as e:
    #     # 接続エラーが発生した場合
    #     handle_log(logger, f"Connection error occurred: {e}")
    # except requests.exceptions.HTTPError as http_error:
    #     # HTTPエラーが発生した場合
    #     handle_log(logger, f"An HTTP error occurred: {http_error}")
    # except requests.exceptions.RequestException as request_error:
    #     # リクエストエラーが発生した場合
    #     handle_log(logger, f"An error occurred during download: {request_error}")
    # except psycopg2.DatabaseError as db_error:
    #     # データベース関連のエラーが発生した場合
    #     handle_log(logger, f"An error occurred in the database: {db_error}")
    # except MissingAPIIdError as missing_api_id_error:
    #     # API IDが指定されていない場合
    #     handle_log(logger, f"Missing API ID: {missing_api_id_error}")
    # except NoMatchingCodeError as no_matching_code_error:
    #     # 対応するコードが存在しない場合
    #     handle_log(logger, f"Target code not found : {no_matching_code_error}")
    # except UnicodeDecodeError as e:
    #     print(f"UnicodeDecodeError: {e}")
    #     print(f"Data that caused the error: {data}")
    #     raise
    # except Exception as general_exception:
    #     # 予期しないその他のエラーが発生した場合
    #     handle_log(logger, f"An unexpected error occurred: {general_exception}")
    # return

    # PostgreSQLの接続情報を環境変数から取得
    db_params = {
        "host": os.environ.get("POSTGRES_HOST"),
        "database": os.environ.get("POSTGRES_DB"),
        "user": os.environ.get("POSTGRES_USER"),
        "password": os.environ.get("POSTGRES_PASSWORD"),
    }

    # ログインを行い、アカウントのインスタンスを作成
    account_instance = login_and_get_account_instance()

    # コードリストを取得
    code_list = get_target_code_list(db_params, os.environ.get("TACHIBANA_USERID"))

    # タスク実行の間隔（秒）
    interval = 0.1
    # 最大の並行タスク数
    max_workers = 10

    # ThreadPoolExecutorを作成
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 15時までのループを開始
        while time.localtime().tm_hour < 15:

            start_time = time.time()
            # execute_tasksを非同期に実行
            executor.submit(execute_task, account_instance, code_list, db_params)

            # 次のタスクがinterval秒後に開始されるように調整
            elapsed_time = time.time() - start_time
            time_to_wait = interval - elapsed_time

            if time_to_wait > 0:
                time.sleep(time_to_wait)

        # 15時になったら最後の1回だけタスクを実行
        executor.submit(execute_task, account_instance, code_list, db_params)
        # ログを表示
        handle_log(logger, "completion: market closure.", logging.INFO)
        return


if __name__ == "__main__":
    main()

# %%
