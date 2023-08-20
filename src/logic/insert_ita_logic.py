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
