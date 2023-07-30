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

    テーブルデータのリスト(table_data)は以下のような辞書型の要素を持つリストです:
    [
        {"sIssueCode": "銘柄コード1", "pDPP": 値1, "pDV": 値2, ... },
        {"sIssueCode": "銘柄コード2", "pDPP": 値1, "pDV": 値2, ... },
        ...
    ]

    Returns:
    dict: 取得した株価データの辞書型

    注意:
    - データベースへの接続 (conn) は関数の外部で作成され、適切にコミットおよびクローズされている必要があります。
    - データベーステーブル (ita_table) は事前に作成されている必要があります。
    - テーブルに存在しないカラムがtable_dataに含まれる場合はエラーが発生します。
    - データの挿入に失敗した場合はロールバックが行われます。

    """

    insert_query = """
        INSERT INTO ita_table (
            code, pdpp, pdv, pprp, pdop, pdhp, pdlp, pvwap, pqap, pqas, pqbp, pqbs, paav, pabv,
            pqov, pquv, pgap10, pgap9, pgap8, pgap7, pgap6, pgap5, pgap4, pgap3, pgap2, pgap1,
            pgbp10, pgbp9, pgbp8, pgbp7, pgbp6, pgbp5, pgbp4, pgbp3, pgbp2, pgbp1, pgav10, pgav9,
            pgav8, pgav7, pgav6, pgav5, pgav4, pgav3, pgav2, pgav1, pgbv10, pgbv9, pgbv8, pgbv7,
            pgbv6, pgbv5, pgbv4, pgbv3, pgbv2, pgbv1
        )
        VALUES (
            %(sIssueCode)s, %(pDPP)s, %(pDV)s, %(pPRP)s, %(pDOP)s, %(pDHP)s, %(pDLP)s, %(pVWAP)s, %(pQAP)s,
            %(pQAS)s, %(pQBP)s, %(pQBS)s, %(pAAV)s, %(pABV)s, %(pQOV)s, %(pQUV)s, %(pGAP10)s, %(pGAP9)s,
            %(pGAP8)s, %(pGAP7)s, %(pGAP6)s, %(pGAP5)s, %(pGAP4)s, %(pGAP3)s, %(pGAP2)s, %(pGAP1)s,
            %(pGBP10)s, %(pGBP9)s, %(pGBP8)s, %(pGBP7)s, %(pGBP6)s, %(pGBP5)s, %(pGBP4)s, %(pGBP3)s,
            %(pGBP2)s, %(pGBP1)s, %(pGAV10)s, %(pGAV9)s, %(pGAV8)s, %(pGAV7)s, %(pGAV6)s, %(pGAV5)s,
            %(pGAV4)s, %(pGAV3)s, %(pGAV2)s, %(pGAV1)s, %(pGBV10)s, %(pGBV9)s, %(pGBV8)s, %(pGBV7)s,
            %(pGBV6)s, %(pGBV5)s, %(pGBV4)s, %(pGBV3)s, %(pGBV2)s, %(pGBV1)s
        )
    """

    try:
        with conn.cursor() as cursor:
            cursor.executemany(insert_query, table_data)
            conn.commit()
            print("Data inserted successfully into ita_table.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
        conn.rollback()
