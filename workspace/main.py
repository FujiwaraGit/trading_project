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
import asyncio
import aiohttp
import httpx

from get_tachibana_api import ClassTachibanaAccount, func_login, func_get_stock_data


URL_BASE = "https://demo-kabuka.e-shiten.jp/e_api_v4r3/"

MY_USERID = "fps04170"  # 自分のユーザーIDに変更してください
MY_PASSWORD = "1997805d"  # 自分のパスワードに変更してください
MY_PASSWORD2 = "1381"  # 自分の第2パスワードに変更してください

CODE_LIST = ["5240", "9227", "3697", "5129"]

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
#             conn.commit()  # データベースの変更をコミット
#             # ロングポーリングを行う非同期関数

async def func_get_api_and_isert_db(tachibana_account, code_list, client ):
    responce_json = func_get_stock_data(tachibana_account, code_list, client )


async def func_insert_roop(tachibana_account):
    """
    ロングポーリングを行う非同期関数

    Returns:
        None
    """
    while True:
        start_time = asyncio.get_event_loop().time()  # ループの開始時刻を取得
        async with httpx.AsyncClient() as client:  # 非同期セッションを作成
            await asyncio.wait_for(
                func_get_api_and_isert_db(tachibana_account, CODE_LIST, client),
                timeout=0.125,
            )  # 0.125秒でタイムアウト
            elapsed_time = asyncio.get_event_loop().time() - start_time  # 処理時間を計測
            if elapsed_time < 0.125:
                await asyncio.sleep(0.125 - elapsed_time)  # 残りの時間をウェイトで待機


async def main():
    """
    メインの処理を実行する関数

    Returns:
        None
    """
    tachibana_account = ClassTachibanaAccount(
        json_fmt='"0"',
        url_base=URL_BASE,
        user_id=MY_USERID,
        password=MY_PASSWORD,
        password_sec=MY_PASSWORD2,
    )  # 立花証券口座インスタンス

    json_response = func_login(tachibana_account)  # ログイン処理を実施

    if not (
        int(json_response.get("p_errno")) == 0
        and len(json_response.get("sUrlEvent") > 0)
    ):  # ログインエラーの場合
        return  # 終了

    # 取得した値を口座属性クラスに設定

    tachibana_account.set_property(
        request_url=json_response.get("sUrlRequest"),
        event_url=json_response.get("sUrlEvent"),
        tax_category=json_response.get("sZyoutoekiKazeiC"),
    )

    async with aiohttp.ClientSession() as session:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(func_insert_roop(tachibana_account))  # 非同期処理を実行


# if __name__ == '__main__':
#     main()

# %%
tachibana_account = ClassTachibanaAccount(
    json_fmt='"0"',
    url_base=URL_BASE,
    user_id=MY_USERID,
    password=MY_PASSWORD,
    password_sec=MY_PASSWORD2,
)  # 立花証券口座インスタンス

# %%
json_response = func_login(tachibana_account)  # ログイン処理を実施


# %%

