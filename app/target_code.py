# %%
import os
import psycopg2

# 取得するデータリスト
CODE_LIST = ["1332", "1605", "1721", "1801", "1803", "1925", "1963", "2002", "2269", "2413", "2432", "2502", "2531", "2768", "2801", "2802", "2871",
             "2914", "3086", "3099", "3101", "3289", "3382", "3402", "3405", "3407", "3436", "3659", "3861", "3863", "4004", "4005", "4042", "4043",
             "4061", "4063", "4151", "4183", "4188", "4208", "4324", "4452", "4502", "4503", "4506", "4507", "4519", "4523", "4543", "4568", "4578",
             "4631", "4689", "4704", "4751", "4755", "4901", "4902", "4911", "5019", "5020", "5101", "5108", "5201", "5202", "5214", "5233", "5301",
             "5332", "5333", "5401", "5406", "5411", "5541", "5631", "5706", "5707", "5711", "5713", "5714", "5801", "5802", "5803", "6098", "6103",
             "6178", "6273", "6301", "6302", "6305", "6326", "6361", "6367", "6471", "6473", "6479", "6501", "6503", "6504", "6506", "6594", "6645",
             "6674", "6701", "6702", "6752", "6753", "6758", "6762", "6770", "6857", "6861", "6902", "6952", "6954", "6971", "6976", "6981", "6988",
             "7003", "7004", "7011", "7012", "7013", "7186", "7201", "7203", "7211", "7261", "7267", "7269", "7270", "7272", "7731", "7733", "7735",
             "7741", "7751", "7752", "7762", "7832", "7911", "7912", "7951", "7974", "8001", "8002", "8015", "8031", "8035", "8053", "8058", "8233",
             "8252", "8253", "8267", "8304", "8306", "8308", "8309", "8316", "8411", "8591", "8601", "8604", "8628", "8630", "8697", "8725", "8750",
             "8766", "8795", "8801", "8802", "8804", "8830", "9005", "9020", "9021", "9064", "9101", "9104", "9107", "9202", "9301", "9432", "9433",
             "9434", "9501", "9502", "9503", "9531", "9532", "9602", "9613", "9735", "9766", "9983", "9984"]


def update_api_id_in_master_stock_table(code_list, api_id_value):
    """
    master_stock_tableの指定されたコードリストに該当する各行のapi_idを更新する関数

    Args:
    code_list (list): 更新対象となるコードリスト
    api_id_value (str): 挿入するapi_idの値

    Returns:
    None
    """
    # PostgreSQLの接続情報を環境変数から取得
    db_params = {
        "host": os.environ.get("POSTGRES_HOST"),
        "database": os.environ.get("POSTGRES_DB"),
        "user": os.environ.get("POSTGRES_USER"),
        "password": os.environ.get("POSTGRES_PASSWORD"),
    }

    # PostgreSQLデータベースに接続する
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    # コードリストに該当する各行にapi_idを挿入
    for code in code_list:
        update_query = "UPDATE master_stock_table SET api_id = %s WHERE code = %s;"
        cursor.execute(update_query, (api_id_value, code))

    # トランザクションをコミットして接続を閉じる
    connection.commit()
    cursor.close()
    connection.close()

    print("api_idを挿入しました。")


def get_codes_by_api_id_value(api_id_value):
    """
    指定したapi_id_valueを持つmaster_stock_tableのcodeを取得する関数

    Args:
    api_id_value (str): 検索対象のapi_idの値

    Returns:
    list: 一致するcodeのリスト
    """
    # PostgreSQLの接続情報を環境変数から取得
    db_params = {
        "host": os.environ.get("POSTGRES_HOST"),
        "database": os.environ.get("POSTGRES_DB"),
        "user": os.environ.get("POSTGRES_USER"),
        "password": os.environ.get("POSTGRES_PASSWORD"),
    }

    # PostgreSQLデータベースに接続する
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    # 指定したapi_id_valueを持つcodeを取得
    select_query = "SELECT code FROM master_stock_table WHERE api_id = %s;"
    cursor.execute(select_query, (api_id_value,))
    codes = [row[0] for row in cursor.fetchall()]

    # 接続を閉じる
    cursor.close()
    connection.close()

    return codes


def main():
    """
    メインの処理を実行する関数

    Returns:
        None
    """
    api_id_value = os.environ.get('TACHIBANA_USERID')
    update_api_id_in_master_stock_table(CODE_LIST, api_id_value)


if __name__ == '__main__':
    main()

# %%
