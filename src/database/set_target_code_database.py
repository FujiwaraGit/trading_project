# -*- coding: utf-8 -*-
"""
このファイルは、データベース内の特定のテーブルの行を更新するための関数を提供するモジュールです。

ファイル内の主な処理ステップ:
1. 必要なモジュールのインポート: データベース操作に必要なモジュールをインポートします。
2. データベース行の更新: データベース内の特定の行を更新する関数を定義します。

注意事項:
- このモジュールは、データベース内の行を更新するための関数を提供します。データベース接続情報が正しく設定されていることを確認してください。
- 更新処理はトランザクション内で行われるため、エラーが発生した場合はロールバックされます。
- 予期せぬエラーが発生した場合、適切な例外が発生し、エラーがログに記録されます。

関連する外部モジュール:
- database.db_connector: データベースへの接続とクエリ実行を行うためのモジュール
"""
from database.db_connector import execute_query


def update_codes_by_api_id(db_params, api_id_value, code):
    """
    データベース行を更新する関数

    Args:
        db_params (dict): データベースへの接続情報が格納された辞書
        data (tuple): 挿入するデータが格納されたタプル

    Returns:
        None
    """
    update_query = "UPDATE master_stock_table SET api_id = %s WHERE code = %s;"
    execute_query(db_params, update_query, (api_id_value, code))
