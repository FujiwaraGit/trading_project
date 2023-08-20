# -*- coding: utf-8 -*-
"""
このファイルは、JPXデータの処理とデータベースへの挿入を行うバッチプロセスを定義しています。
JPX（日本取引所グループ）関連のデータを取得し、処理してデータベースに挿入する機能が実装されています。

ファイルの概要:
このファイルは、以下の主な機能を提供します。
- JPX関連のデータを取得して処理します。
- 取得したデータを指定されたデータベースに挿入します。
- エラーハンドリングを行い、異常終了時にログを記録します。

ファイル内の主な処理ステップ:
1. 必要なライブラリをインポートします。
2. ログの設定や操作を行う関数をインポートします。
3. メイン関数 `main()` を定義します。この関数が処理の中心です。
4. ログ設定を行い、処理の開始をログに記録します。
5. JPXデータの取得と処理を行います。
6. PostgreSQLの接続情報を環境変数から取得し、データベースに挿入します。
7. IPOデータを取得してデータベースに挿入します。
8. 処理の正常終了をログに記録します。
9. エラーハンドリングを行い、例外が発生した場合にログにエラー内容を記録します。

このファイルは、バッチプロセスとして実行されることを想定しており、JPXデータの自動処理を行う際に利用されます。
"""
# %%
# 必要なライブラリのインポート
import os
import logging
import requests
import pandas as pd
import psycopg2
from logic.set_code_logic import make_jpx_df, update_jpx_to_db, make_ipo_df, insert_ipo_to_db
from log.logging_config import configure_logging
from utilities.utility import handle_log


def main():
    """
    メイン関数：JPXデータの処理とデータベースへの挿入を実行します。
    """

    # ログ設定
    log_filename = "/src/log/code_list_batch.log"
    logger = configure_logging(log_filename)

    # 開始のログを出力
    handle_log(logger, f"start: {__name__}", logging.INFO)

    try:
        # JPXデータの取得と処理
        df_jpx = make_jpx_df()

        # PostgreSQLの接続情報を環境変数から取得
        db_params = {
            "host": os.environ.get("POSTGRES_HOST"),
            "database": os.environ.get("POSTGRES_DB"),
            "user": os.environ.get("POSTGRES_USER"),
            "password": os.environ.get("POSTGRES_PASSWORD"),
        }

        # データをデータベースに挿入
        update_jpx_to_db(db_params, df_jpx)

        # IPOデータを取得してデータベースに挿入
        df_ipo = make_ipo_df()

        insert_ipo_to_db(db_params, df_ipo)

        # 正常終了ログを出力
        handle_log(logger, "completion: All processes have terminated successfully.", logging.INFO)

    # エラーハンドリング
    except requests.exceptions.Timeout as e:
        # リクエストがタイムアウトした場合
        handle_log(logger, f"Request timed out: {e}")
    except requests.exceptions.ConnectionError as e:
        # 接続エラーが発生した場合
        handle_log(logger, f"Connection error occurred: {e}")
    except requests.exceptions.HTTPError as http_error:
        # HTTPエラーが発生した場合
        handle_log(logger, f"An HTTP error occurred: {http_error}")
    except requests.exceptions.RequestException as request_error:
        # リクエストエラーが発生した場合
        handle_log(logger, f"An error occurred during download: {request_error}")
    except FileNotFoundError as file_not_found:
        # ファイルが見つからない場合
        handle_log(logger, f"File not found: {file_not_found}")
    except pd.errors.ParserError as parser_error:
        # Excelファイルの解析エラーが発生した場合
        handle_log(logger, f"Error parsing Excel file: {parser_error}")
    except OSError as os_error:
        # OS関連のエラーが発生した場合
        handle_log(logger, f"Error during file deletion: {os_error}")
    except ValueError as value_error:
        # 値の処理に関するエラーが発生した場合
        handle_log(logger, f"Value error occurred: {value_error}")
    except psycopg2.DatabaseError as db_error:
        # データベース関連のエラーが発生した場合
        handle_log(logger, f"An error occurred in the database: {db_error}")
    except Exception as general_exception:
        # 予期しないその他のエラーが発生した場合
        handle_log(logger, f"An unexpected error occurred: {general_exception}")

if __name__ == "__main__":
    main()

# %%
