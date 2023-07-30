# %%
import os
import time
import multiprocessing
import psycopg2
from get_tachibana_api import func_get_stock_data, func_login_and_get_account_instance
from insert_data_to_pg import func_insert_stock_data_into_table


# 取得するデータリスト
CODE_LIST = ["1332", "1605", "1721", "1801", "1803", "1925", "1963", "2002", "2269", "2413", "2432", "2502", "2531", "2768", "2801", "2802", "2871", "2914", "3086", "3099", "3101", "3289", "3382", "3402", "3405", "3407", "3436", "3659", "3861", "3863", "4004", "4005", "4042", "4043", "4061", "4063", "4151", "4183", "4188", "4208", "4324", "4452", "4502", "4503", "4506", "4507", "4519", "4523", "4543", "4568", "4578", "4631", "4689", "4704", "4751", "4755", "4901", "4902", "4911", "5019", "5020", "5101", "5108", "5201", "5202", "5214", "5233", "5301", "5332", "5333", "5401", "5406", "5411", "5541", "5631", "5706", "5707", "5711", "5713", "5714", "5801", "5802", "5803", "6098", "6103", "6178", "6273", "6301", "6302", "6305", "6326", "6361", "6367", "6471", "6473", "6479", "6501", "6503", "6504", "6506", "6594", "6645", "6674", "6701", "6702", "6752", "6753", "6758", "6762", "6770", "6857", "6861", "6902", "6952", "6954", "6971", "6976", "6981", "6988", "7003", "7004", "7011", "7012", "7013", "7186", "7201", "7203", "7211", "7261", "7267", "7269", "7270", "7272", "7731", "7733", "7735", "7741", "7751", "7752", "7762", "7832", "7911", "7912", "7951", "7974", "8001", "8002", "8015", "8031", "8035", "8053", "8058", "8233", "8252", "8253", "8267", "8304", "8306", "8308", "8309", "8316", "8411", "8591", "8601", "8604", "8628", "8630", "8697", "8725", "8750", "8766", "8795", "8801", "8802", "8804", "8830", "9005", "9020", "9021", "9064", "9101", "9104", "9107", "9202", "9301", "9432", "9433", "9434", "9501", "9502", "9503", "9531", "9532", "9602", "9613", "9735", "9766", "9983", "9984"]

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

        # 現在の時刻を取得
        current_time = time.localtime()
        if current_time.tm_hour >= 15:
            break


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

        # 現在の時刻を取得
        current_time = time.localtime()
        if current_time.tm_hour >= 15:
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
