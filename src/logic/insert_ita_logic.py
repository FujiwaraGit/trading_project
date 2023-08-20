# -*- coding: utf-8 -*-
"""
このファイルは、データベース操作やHTTPリクエストを使用して特定のタスクを実行する関数を提供するモジュールです。

ファイル内の主な処理ステップ:
1. 必要なモジュールのインポート: データベース操作やHTTPリクエストに必要なモジュールをインポートします。
2. タスクの実行: 指定されたアカウントインスタンスやコードリスト、接続情報を使用してタスクを実行する関数を定義します。
3. 対象の証券コードリストの取得: 指定されたapi_id_valueを持つmaster_stock_tableのコードを取得する関数を定義します。
4. ログインとインスタンス取得: ログインを行い、立花証券口座クラスのインスタンスを取得する関数を定義します。

注意事項:
- このモジュールは、データベース操作やHTTPリクエストを使用して特定のタスクを実行する関数を提供します。必要なモジュールや設定が正しく行われていることを確認してください。
- タスクの実行中にエラーが発生した場合、適切な例外が発生し、エラーがログに記録されます。

提供される関数:
- execute_task: 指定されたアカウントインスタンスやコードリスト、接続情報を使用してタスクを実行する関数
- get_target_code_list: 指定したapi_id_valueを持つmaster_stock_tableのcodeを取得する関数
- login: ログインを行い、立花証券口座クラスのインスタンスを返す関数

関数の引数や戻り値についての詳細な説明が記述されています。

関連する外部モジュール:
- database.insert_ita_database: データベースへのデータ挿入に関するモジュール
- http_requests.insert_ita_requests: HTTPリクエストを使用して株価データを取得するモジュール
- utilities.custom_exceptions: カスタム例外クラスを提供するモジュール
"""

from database.insert_ita_database import insert_rows, search_codes_by_api_id
from http_requests.insert_ita_requests import get_stock_data, login_and_get_account_instance
from utilities.custom_exceptions import MissingAPIIdError, NoMatchingCodeError


def execute_task(account_instance, code_list, db_params):
    """
    タスクを実行する関数

    Args:
        account_instance (object): アカウントのインスタンス
            APIにアクセスするためのアカウント情報を持つインスタンスです。
        code_list (list): 取得するデータリスト
            取得したい証券コードのリストです。APIからこれらの証券コードに対応する株価データを取得します。
        connection (psycopg2.Connection): PostgreSQLへの接続情報
            データをデータベースに保存するためのPostgreSQLの接続情報です。

    Returns:
        None
    """
    # 証券コードに対応する株価データを取得
    return_json = get_stock_data(account_instance, code_list)
    # 取得した株価データをデータベースに挿入
    insert_rows(db_params, return_json)


def get_target_code_list(db_params, api_id_value):
    """
    指定したapi_id_valueを持つmaster_stock_tableのcodeを取得する関数

    Args:
    api_id_value (str): 検索対象のapi_idの値

    Returns:
    list: 一致するcodeのリスト
    """

    # 引数がNoneのとき例外発生
    if api_id_value is None:
        raise MissingAPIIdError("api_id_value is None")

    result = search_codes_by_api_id(db_params, api_id_value)
    codes = [row[0] for row in result]

    # 取得したcodeが0行の場合、例外を発生させる
    if len(codes) == 0:
        raise NoMatchingCodeError("The code_list is 0 lines.")

    # 取得したcodeを返す
    return codes


def login():
    """
    ログインを行い、立花証券口座クラスのインスタンスを返す関数

    Returns:
        ClassTachibanaAccount: tachiban口座属性クラスのインスタンス
    """
    return login_and_get_account_instance()
