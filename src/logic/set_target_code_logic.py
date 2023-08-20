# -*- coding: utf-8 -*-
"""
このファイルは、指定されたデータベース内の特定のテーブルに対してコードの更新を行うためのスクリプトです。

ファイル内の主な処理ステップ:
1. 必要なモジュールのインポート: PostgreSQLデータベースへの接続やコードの更新に必要なモジュールをインポートします。
2. コードリストの取得: 指定されたapi_id_valueを持つmaster_stock_tableのコードを取得する関数を定義します。
3. コードの更新: master_stock_tableの指定されたコードリストに該当する各行のapi_idを更新する関数を定義します。

注意事項:
- このスクリプトは、特定のデータベースに対してコードの更新を行います。正確なデータベース接続情報やコードリストが提供されていることを確認してください。
- コードの更新はトランザクション内で行われるため、エラーが発生した場合はロールバックされます。
- 予期せぬエラーが発生した場合、適切な例外が発生し、エラーがログに記録されます。

ファイルの構成:
- データベース接続やコード更新に関する関数の定義
- 主処理関数 (update_target_codes) の定義

関連する外部モジュール:
- psycopg2: PostgreSQLデータベースへの接続と操作を行うためのモジュール
- database.set_target_code_database: データベース内でコード更新を行うためのモジュール

"""

import psycopg2
from database.set_target_code_database import update_codes_by_api_id


def get_target_code_list(api_id_value, connection):
    """
    指定したapi_id_valueを持つmaster_stock_tableのcodeを取得する関数

    Args:
    api_id_value (str): 検索対象のapi_idの値

    Returns:
    list: 一致するcodeのリスト
    """

    # 引数がNoneのとき例外発生
    if api_id_value is None:
        raise Exception("api_id_value is None")

    try:
        # PostgreSQLデータベースに接続し、トランザクション内で操作を行う
        with connection.cursor() as cursor:
            # 指定したapi_id_valueを持つcodeを取得するためのクエリを実行
            select_query = "SELECT code FROM master_stock_table WHERE api_id = %s;"
            cursor.execute(select_query, (api_id_value,))
            codes = [row[0] for row in cursor.fetchall()]
    except (Exception, psycopg2.DatabaseError) as error:
        # 例外が発生した場合、そのまま上位のスコープに例外を伝播させる
        raise error

    # 取得したcodeが0行の場合、例外を発生させる
    if len(codes) == 0:
        raise Exception("The code_list is 0 lines.")

    # 取得したcodeを返す
    return codes


def update_target_codes(db_params, code_list, api_id_value):
    """
    master_stock_tableの指定されたコードリストに該当する各行のapi_idを更新する関数

    Args:
    code_list (list): 更新対象となるコードリスト
    api_id_value (str): 挿入するapi_idの値

    Returns:
    None
    """

    # コードリストに該当する各行にapi_idを挿入
    for code in code_list:
        update_codes_by_api_id(db_params, api_id_value, code)
