# -*- coding: utf-8 -*-
"""
リアルタイムの株価データをデータベースに挿入するスクリプト

このスクリプトは、リアルタイムの株価データを取得し、指定されたデータベーステーブルに挿入するための関数を提供します。
関数 `func_insert_stock_data_into_table` は以下の引数を受け取り、株価データをテーブルに挿入します:

- table_data: テーブルデータのリスト。各要素は株価データを表す辞書です。
- conn: データベースへの接続オブジェクト。コネクションは関数外で作成し、正しくコミットおよびクローズされている必要があります。

注意事項:
- データベーステーブル (`ita_table`) は事前に作成されている必要があります。
- `table_data` に含まれるカラムは、テーブルのカラムと一致する必要があります。
- データの挿入に失敗した場合は、トランザクションがロールバックされます。

"""
import datetime
from database.db_connector import execute_query


def search_codes_by_api_id(db_params, api_id_value):
    """
    指定されたAPI IDの値を持つマスターストックテーブルのコードを検索し、結果を返す関数。

    Args:
    db_params (dict): データベース接続のためのパラメータ
    api_id_value (str): 検索対象のAPI IDの値

    Returns:
    list: 一致するコードのリスト
    """
    select_query = "SELECT code FROM master_stock_table WHERE api_id = %s;"
    result = execute_query(db_params, select_query, (api_id_value,), True)
    return result


def insert_rows(db_params, data):
    """
    データベースに行を挿入する関数。

    Args:
    db_params (dict): データベース接続のためのパラメータ
    data (dict): 挿入するデータの辞書。キーに対応するカラム名と値を含む。

    Returns:
    None
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
    execute_query(db_params, insert_query, data, False, True)
    print("insert sucsess: ", datetime.datetime.now())
    return
