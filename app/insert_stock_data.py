#%%
import asyncio
import aiohttp
import sqlite3
from datetime import datetime

# データベースの接続とテーブルの作成
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS data (timestamp TEXT, value INTEGER)')

# APIからデータを非同期に取得してDBに格納する関数
async def fetch_data(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()  # レスポンスからJSONデータを取得
            timestamp= datetime.now().isoformat()  # 現在のタイムスタンプを取得
            value = data['value']  # データから必要な値を抽出
            cursor.execute('INSERT INTO data (timestamp, value) VALUES (?, ?)', (timestamp, value))  # データをデータベースに挿入
            conn.commit()  # データベースの変更をコミット

# ロングポーリングを行う非同期関数
async def long_polling():
    url = 'http://example.com/api/data'  # データを提供するAPIのエンドポイントを指定
    while True:
        start_time = asyncio.get_event_loop().time()  # ループの開始時刻を取得
        async with aiohttp.ClientSession() as session:  # 非同期セッションを作成
            task = fetch_data(session, url)  # データの取得とデータベースへの格納を非同期に実行
            await asyncio.wait_for(task, timeout=0.125)  # 0.125秒でタイムアウト
        elapsed_time = asyncio.get_event_loop().time() - start_time  # 処理時間を計測
        if elapsed_time < 0.125:
            await asyncio.sleep(0.125 - elapsed_time)  # 残りの時間をウェイトで待機

# # メインの処理
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(long_polling())  # 非同期処理を実行

#%%
