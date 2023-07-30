# %%
import os
import time
import concurrent.futures
import psycopg2
import get_tachibana_api
import insert_data_to_pg
import target_code
import utility


# PostgreSQLの接続情報を環境変数から取得
db_params = {
    "host": os.environ.get("POSTGRES_HOST"),
    "database": os.environ.get("POSTGRES_DB"),
    "user": os.environ.get("POSTGRES_USER"),
    "password": os.environ.get("POSTGRES_PASSWORD"),
}


def execute_task(account_instance, code_list, connection):
    """
    タスクを実行する関数

    Args:
        account_instance (object): アカウントのインスタンス
            APIにアクセスするためのアカウント情報を持つインスタンスです。
        code_list (list): 取得するデータリスト
            取得したい証券コードのリストです。APIからこれらの証券コードに対応する株価データを取得します。
        connection (psycopg2.Connection): PostgreSQLへの接続情報
            データをデータベースに保存するためのPostgreSQLの接続情報です。

    Returns:
        None
    """

    # 証券コードに対応する株価データを取得
    return_json = get_tachibana_api.func_get_stock_data(account_instance, code_list)

    # 取得した株価データをデータベースに挿入
    insert_data_to_pg.func_insert_stock_data_into_table(return_json, connection)


def execute_tasks_in_loop(account_instance, code_list, connection, interval=0.125, max_workers=10):
    """
    タスクを定期的に実行する関数

    Args:
        account_instance (object): アカウントのインスタンス
        code_list (list): 取得するデータリスト
        connection (psycopg2.Connection): PostgreSQLへの接続情報
        interval (float): タスク実行の間隔（秒）
        max_workers (int): 最大の並行タスク数

    Returns:
        None
    """
    # ThreadPoolExecutorを作成
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 15時までのループを開始
        while time.localtime().tm_hour < 15:
            start_time = time.time()

            # execute_tasksを非同期に実行
            executor.submit(execute_task, account_instance, code_list, connection)

            # 次のタスクがinterval秒後に開始されるように調整
            elapsed_time = time.time() - start_time
            time_to_wait = interval - elapsed_time

            if time_to_wait > 0:
                time.sleep(time_to_wait)

        # 15時になったら最後の1回だけタスクを実行
        executor.submit(execute_task, account_instance, code_list, connection)

    # PostgreSQLの接続をクローズ
    connection.close()


def main():
    """
    メインの処理を実行する関数

    Returns:
        None
    """

    # 本日休日なら終了
    if(utility.is_today_holiday() is True):
        return

    # ログインを行い、アカウントのインスタンスを作成
    account_instance = get_tachibana_api.func_login_and_get_account_instance()

    # ログイン失敗時の処理
    if account_instance is None:
        print("ログインに失敗しました。プログラムを終了します。")
        return

    # PostgreSQLに接続
    connection = psycopg2.connect(**db_params)

    # code_listを取得
    api_id_value = os.environ.get('TACHIBANA_USERID')
    code_list = target_code.get_codes_by_api_id_value(api_id_value)

    if connection:
        # マルチプロセスでタスクを実行
        execute_tasks_in_loop(account_instance, code_list, connection)


if __name__ == '__main__':
    main()

# %%
