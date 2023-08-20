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
import concurrent.futures
import psycopg2
from database import insert_ita_database
from utilities import utility
from logic import target_code_entry

# ログ設定
LOG_FILENAME = "/app/log/insert_ita.log"
if not os.path.exists(LOG_FILENAME):
    open(LOG_FILENAME, "w", encoding="utf-8")  # ファイルが存在しない場合、空のファイルを作成

logging.basicConfig(
    filename=LOG_FILENAME,  # ファイル名を指定
    level=logging.DEBUG,  # 出力レベルを設定
    format="%(asctime)s - %(levelname)s - %(message)s",
)
# loggerのインスタンス化
logger = logging.getLogger(__name__)

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
    return_json = insert_ita_api.func_get_stock_data(account_instance, code_list)
    # 取得した株価データをデータベースに挿入
    insert_ita_database.func_insert_stock_data_into_table(return_json, connection)


def execute_tasks_in_loop(
    account_instance, code_list, connection, interval=0.1, max_workers=10
):
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
        return


def main():
    """
    メインの処理を実行する関数

    Returns:
        None
    """

    # 開始のログを出力
    logger.info("start: " + __name__)
    print("start: " + __name__)

    # 本日休日なら終了
    if utility.is_today_holiday() is True:
        print("completion: Closed due to a holiday.")
        logger.info("completion: Closed due to a holiday.")
        return

    try:
        # ログインを行い、アカウントのインスタンスを作成
        account_instance = insert_ita_api.func_login_and_get_account_instance()

        # PostgreSQLに接続
        with psycopg2.connect(**db_params) as connection:
            # コードリストを取得
            code_list = target_code_entry.get_codes_by_api_id_value(
                os.environ.get("TACHIBANA_USERID"), connection
            )

            # マルチプロセスでタスクを実行
            execute_tasks_in_loop(account_instance, code_list, connection)

    except Exception as error:
        # エラーをログに記録
        logger.error("Interruption: " + str(error))
        # エラーメッセージをコンソールに表示
        print("Interruption:", error)
        return

    # 15時になったら正常終了
    print("completion: market closure.")
    logger.info("completion: market closure.")


if __name__ == "__main__":
    main()

# %%