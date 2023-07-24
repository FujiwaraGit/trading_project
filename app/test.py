# %%
import psycopg2

#%%
# PostgreSQLに接続
connection = psycopg2.connect(
    host='db',
    port='5432',
    database='mydatabase',
    user='myuser',
    password='mypassword'
)

# カーソルを作成
cursor = connection.cursor()

# クエリを実行
cursor.execute("SELECT * FROM mytable;")

# 結果を取得
results = cursor.fetchall()

# 結果を表示
for row in results:
    print(row)

# 接続を閉じる
cursor.close()
connection.close()

# %%
