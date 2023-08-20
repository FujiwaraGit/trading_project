# -*- coding: utf-8 -*-
"""
このファイルは、特定のデータベース内のコードリストを更新するためのスクリプトです。
指定されたコードリストを使用して、対象となるコードをデータベース内で更新します。

ファイル内の主な処理ステップ:
1. ログの設定: ログファイルへの情報の記録を行います。
2. データベース接続情報の取得: 環境変数からPostgreSQLデータベースへの接続情報を取得します。
3. コードリストの定義: 更新する対象のコードリストを事前に定義しています。
4. 主処理の実行: 定義されたコードリストを使用して、データベース内の対象コードを更新します。

注意事項:
- このスクリプトは、特定のデータベースに対してコードの更新を行います。正確なデータベース接続情報やコードリストが提供されていることを確認してください。
- 予期せぬエラーが発生した場合、適切なログが記録されます。
- メイン処理の実行後、更新が完了したことを示すログが出力されます。

ファイルの構成:
- PostgreSQLデータベースへの接続情報
- 更新対象となるコードリスト
- メイン関数の実行とログ出力

"""

# %%
import os
import logging
import psycopg2
from logic.set_target_code_logic import update_target_codes
from log.logging_config import configure_logging
from utilities.utility import handle_log

# 取得するデータリスト
CODE_LIST = ["1332", "1605", "1721", "1801", "1803", "1925", "1963", "2002",
             "2269", "2413", "2432", "2502", "2531", "2768", "2801", "2802",
             "2871", "2914", "3086", "3099", "3101", "3289", "3382", "3402",
             "3405", "3407", "3436", "3659", "3861", "3863", "4004", "4005",
             "4042", "4043", "4061", "4063", "4151", "4183", "4188", "4208",
             "4324", "4452", "4502", "4503", "4506", "4507", "4519", "4523",
             "4543", "4568", "4578", "4631", "4689", "4704", "4751", "4755",
             "4901", "4902", "4911", "5019", "5020", "5101", "5108", "5201",
             "5202", "5214", "5233", "5301", "5332", "5333", "5401", "5406",
             "5411", "5541", "5631", "5706", "5707", "5711", "5713", "5714",
             "5801", "5802", "5803", "6098", "6103", "6178", "6273", "6301",
             "6302", "6305", "6326", "6361", "6367", "6471", "6473", "6479",
             "6501", "6503", "6504", "6506", "6594", "6645", "6674", "6701",
             "6702", "6752", "6753", "6758", "6762", "6770", "6857", "6861",
             "6902", "6952", "6954", "6971", "6976", "6981", "6988", "7003",
             "7004", "7011", "7012", "7013", "7186", "7201", "7203", "7211",
             "7261", "7267", "7269", "7270", "7272", "7731", "7733", "7735",
             "7741", "7751", "7752", "7762", "7832", "7911", "7912", "7951",
             "7974", "8001", "8002", "8015", "8031", "8035", "8053", "8058",
             "8233", "8252", "8253", "8267", "8304", "8306", "8308", "8309",
             "8316", "8411", "8591", "8601", "8604", "8628", "8630", "8697",
             "8725", "8750", "8766", "8795", "8801", "8802", "8804", "8830",
             "9005", "9020", "9021", "9064", "9101", "9104", "9107", "9202",
             "9301", "9432", "9433", "9434", "9501", "9502", "9503", "9531",
             "9532", "9602", "9613", "9735", "9766", "9983", "9984"]


def main():
    """
    メインの処理を実行する関数

    Returns:
        None
    """
    # ログ設定
    log_filename = "/src/log/set_target_code.log"
    logger = configure_logging(log_filename)

    # 開始のログを出力
    handle_log(logger, f"start: {__name__}", logging.INFO)

    try:
        # PostgreSQLの接続情報を環境変数から取得
        db_params = {
            "host": os.environ.get("POSTGRES_HOST"),
            "database": os.environ.get("POSTGRES_DB"),
            "user": os.environ.get("POSTGRES_USER"),
            "password": os.environ.get("POSTGRES_PASSWORD"),
        }

        # コードリストを取得
        # code_list = get_target_code_list(db_params, os.environ.get("TACHIBANA_USERID"))

        api_id_value = os.environ.get('TACHIBANA_USERID')
        update_target_codes(db_params, CODE_LIST, api_id_value)
    except psycopg2.DatabaseError as db_error:
        # データベース関連のエラーが発生した場合
        handle_log(logger, f"An error occurred in the database: {db_error}")
    except Exception as general_exception:
        # 予期しないその他のエラーが発生した場合
        handle_log(logger, f"An unexpected error occurred: {general_exception}")

    # ログを表示
    handle_log(logger, "completion: update_code", logging.INFO)
    return


if __name__ == '__main__':
    main()

# %%
