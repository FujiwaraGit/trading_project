# %%
import os
import time
import multiprocessing
import psycopg2
from get_tachibana_api import func_get_stock_data, func_login_and_get_account_instance
from insert_data_to_pg import func_insert_stock_data_into_table


# 取得するデータリスト
CODE_LIST = ["5240", "9227", "3697", "5129"]

# PostgreSQLの接続情報を環境変数から取得
db_params = {
    "host": os.environ.get("POSTGRES_HOST"),
    "database": os.environ.get("POSTGRES_DB"),
    "user": os.environ.get("POSTGRES_USER"),
    "password": os.environ.get("POSTGRES_PASSWORD"),
}


def execute_tasks(account_instance, code_list, connection):
    """
    タスクを実行する関数

    Args:
        account_instance (object): アカウントのインスタンス
        code_list (list): 取得するデータリスト
        connection (psycopg2.Connection): PostgreSQLへの接続情報

    Returns:
        None
    """
    while True:
        start_time = time.time()

        return_json = func_get_stock_data(account_instance, code_list)
        func_insert_stock_data_into_table(return_json, connection)

        elapsed_time = time.time() - start_time

        if elapsed_time < 0.125:
            time.sleep(0.125 - elapsed_time)


def execute_tasks_with_multiprocessing(account_instance, code_list, connection):
    """
    マルチプロセスでタスクを実行する関数

    Args:
        account_instance (object): アカウントのインスタンス
        code_list (list): 取得するデータリスト
        connection (psycopg2.Connection): PostgreSQLへの接続情報

    Returns:
        None
    """
    process = multiprocessing.Process(target=execute_tasks, args=(account_instance, code_list, connection))
    process.start()

    while True:
        try:
            # メインプロセスがここで待機することで、マルチプロセスが継続して実行される
            process.join(0.125)
        except KeyboardInterrupt:
            # Ctrl+Cが押された場合、マルチプロセスを終了させる
            process.terminate()
            process.join()
            break


def main():
    """
    メインの処理を実行する関数

    Returns:
        None
    """
    # ログインを行い、アカウントのインスタンスを作成
    account_instance = func_login_and_get_account_instance()

    # ログイン失敗時の処理
    if account_instance is None:
        print("ログインに失敗しました。プログラムを終了します。")
        return

    # PostgreSQLに接続
    connection = psycopg2.connect(**db_params)

    if connection:
        execute_tasks_with_multiprocessing(account_instance, CODE_LIST, connection)


if __name__ == '__main__':
    main()

# %%
