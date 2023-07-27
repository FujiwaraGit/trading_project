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

# %%
# async def fetch_data(session, url):
#     """
#     APIからデータを非同期に取得してDBに格納する関数

#     Args:
#         session (aiohttp.ClientSession): Aiohttpのクライアントセッション
#         url (str): データを提供するAPIのエンドポイント

#     Returns:
#         None
#     """
#     async with session.get(url) as response:
#         if response.status == 200:
#             data = await response.json()  # レスポンスからJSONデータを取得
#             timestamp = datetime.now().isoformat()  # 現在のタイムスタンプを取得
#             value = data['value']  # データから必要な値を抽出
#             cursor.execute('INSERT INTO data (timestamp, value) VALUES (?, ?)', (timestamp, value))  # データをデータベースに挿入


# def func_insert_roop(tachibana_account):
#     """
#     ロングポーリングを行う非同期関数

#     Returns:
#         None
#     """
#     while True:
#         start_time = asyncio.get_event_loop().time()  # ループの開始時刻を取得
#         async with httpx.AsyncClient() as client:  # 非同期セッションを作成
#             await asyncio.wait_for(
#                 func_get_api_and_isert_db(tachibana_account, CODE_LIST, client),
#                 timeout=0.125,
#             )  # 0.125秒でタイムアウト
#             elapsed_time = asyncio.get_event_loop().time() - start_time  # 処理時間を計測
#             if elapsed_time < 0.125:
#                 await asyncio.sleep(0.125 - elapsed_time)  # 残りの時間をウェイトで待機


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
        func_insert_stock_data_into_table(db_params, return_json, connection)
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)
    finally:
        if connection:
            connection.close()


if __name__ == '__main__':
    main()

# %%
