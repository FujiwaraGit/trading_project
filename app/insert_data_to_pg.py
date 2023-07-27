import psycopg2


def func_insert_stock_data_into_table(table_data, conn):
    """
    リアルタイムの株価データを取得する関数

    Args:
    url_base (str): データを取得するAPIのベースURL
    user_id (str): 立花証券のユーザーID
    password (str): 立花証券のパスワード
    password2 (str): 立花証券の第2パスワード
    code_list (list): 株価データを取得する銘柄コードのリスト

    Returns:
    dict: 取得した株価データの辞書型
    """
    # テーブルにデータをINSERTするSQLクエリ
    insert_query = """
        INSERT INTO ita_table (
            code, pdpp, pdv, pprp, pdop, pdhp, pdlp, pvwap, pqap, pqas, pqbp, pqbs, paav, pabv,
            pqov, pquv, pgap10, pgap9, pgap8, pgap7, pgap6, pgap5, pgap4, pgap3, pgap2, pgap1,
            pgbp10, pgbp9, pgbp8, pgbp7, pgbp6, pgbp5, pgbp4, pgbp3, pgbp2, pgbp1, pgav10, pgav9,
            pgav8, pgav7, pgav6, pgav5, pgav4, pgav3, pgav2, pgav1, pgbv10, pgbv9, pgbv8, pgbv7,
            pgbv6, pgbv5, pgbv4, pgbv3, pgbv2, pgbv1
        )
        VALUES (
            %(code)s, %(pdpp)s, %(pdv)s, %(pprp)s, %(pdop)s, %(pdhp)s, %(pdlp)s, %(pvwap)s, %(pqap)s,
            %(pqas)s, %(pqbp)s, %(pqbs)s, %(paav)s, %(pabv)s, %(pqov)s, %(pquv)s, %(pgap10)s, %(pgap9)s,
            %(pgap8)s, %(pgap7)s, %(pgap6)s, %(pgap5)s, %(pgap4)s, %(pgap3)s, %(pgap2)s, %(pgap1)s,
            %(pgbp10)s, %(pgbp9)s, %(pgbp8)s, %(pgbp7)s, %(pgbp6)s, %(pgbp5)s, %(pgbp4)s, %(pgbp3)s,
            %(pgbp2)s, %(pgbp1)s, %(pgav10)s, %(pgav9)s, %(pgav8)s, %(pgav7)s, %(pgav6)s, %(pgav5)s,
            %(pgav4)s, %(pgav3)s, %(pgav2)s, %(pgav1)s, %(pgbv10)s, %(pgbv9)s, %(pgbv8)s, %(pgbv7)s,
            %(pgbv6)s, %(pgbv5)s, %(pgbv4)s, %(pgbv3)s, %(pgbv2)s, %(pgbv1)s
        )
    """

    try:
        with conn.cursor() as cursor:
            # table_dataのデータをita_tableに一括INSERT
            for item in table_data["aCLMMfdsMarketPrice"]:
                cursor.execute(insert_query, item)
            conn.commit()
            print("Data inserted successfully into ita_table.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
        conn.rollback()
