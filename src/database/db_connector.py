# -*- coding: utf-8 -*-
"""
このファイルは、データベース操作に関する関数を提供するモジュールです。

ファイル内の主な処理ステップ:
1. 必要なモジュールのインポート: データベースへの接続とクエリ実行に必要なモジュールをインポートします。
2. データベースへのクエリ実行: データベースに接続して指定されたSQLクエリを実行する関数を定義します。

注意事項:
- このモジュールは、データベース操作に関する関数を提供します。データベース接続情報やクエリが正しく設定されていることを確認してください。
- クエリの実行中にエラーが発生した場合、適切な例外が発生し、エラーがログに記録されます。

"""
import psycopg2


def execute_query(db_params, query, data=None, fetch=False, use_executemany=False):
    """
    データベースに接続してSQLクエリを実行する関数

    Args:
    db_params (dict): データベースへの接続情報が格納された辞書
    query (str): 実行するSQLクエリ
    data (tuple): クエリに渡すデータ（省略可能）
    fetch (bool): クエリ結果を取得するかどうか（省略可能）

    Returns:
    None or list: fetchがTrueの場合、クエリ結果のリストを返す
    """
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                if data:
                    if use_executemany:
                        cursor.executemany(query, data)
                    else:
                        cursor.execute(query, data)
                else:
                    cursor.execute(query)
                conn.commit()
                if fetch:
                    return cursor.fetchall()
                return
    except psycopg2.DatabaseError as error:
        conn.rollback()
        raise error
