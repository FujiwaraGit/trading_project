# %%
"""
立花証券のAPIを使用して株式データを取得するPythonプログラムです。

使用方法:

自分のユーザーID、パスワード、第2パスワードを変数に設定してください。
CODE_LISTに取得したい株式の銘柄コードをリストとして追加してください。
プログラムを実行してください。
注意事項:

ログインが成功した場合、株式データを取得します。
応答データはJSON形式で返されます。
ログインに成功した場合、応答データには取得した株式データが含まれます。
"""
import os
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
        # 現状ただの終了にしているが、アラートなど改良余地あり
        return

    # 株式データを取得
    return_json = func_get_stock_data(account_instance, CODE_LIST)

    # PostgreSQLに接続
    try:
        connection = psycopg2.connect(**db_params)
        # データをinsert
        func_insert_stock_data_into_table(return_json, connection)
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)
    finally:
        if connection:
            connection.close()


if __name__ == '__main__':
    main()

# %%

db_params

# %%
