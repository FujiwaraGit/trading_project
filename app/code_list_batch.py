# -*- coding: utf-8 -*-
"""
ファイル説明:
このPythonスクリプトは、東証から株価データをダウンロードして整形し、PostgreSQLデータベースに挿入する機能を提供します。
また、ウェブサイトから新しいIPO（新規公開株）データを抽出し、データベースに挿入する機能も含まれています。

関数の概要:
- get_jpx_data(): 東証から株価データをダウンロードして取得する関数
- preprocess_data(df): ダウンロードした株価データを整形する関数
- insert_data_to_table(df, db_params): 株価データをデータベースにInsertかUpdateする関数
- fetch_html_content(url): 指定されたURLからHTMLコードを取得する関数
- parse_html_to_dataframe(html_content): HTMLコードからIPOデータを抽出して整形する関数
- insert_new_rows_to_database(df, db_params): 新しいIPOデータをデータベースに挿入する関数
- main(): メインの実行関数

ファイルの使い方:
1. ダウンロードしたい株価データのURLを `url` 変数に設定します。
2. PostgreSQLデータベースの接続情報を環境変数に設定します。
3. スクリプトを実行して、株価データを取得し、PostgreSQLデータベースに挿入します。
4. ウェブサイトからIPOデータを取得し、新しいIPOデータをデータベースに挿入します。
"""

# %%
import os
import logging
import pandas as pd
import jaconv
import requests
import psycopg2
from bs4 import BeautifulSoup

# ログ設定
LOG_FILENAME = "/app/log/code_list_batch.log"
if not os.path.exists(LOG_FILENAME):
    open(LOG_FILENAME, "w", encoding="utf-8")  # ファイルが存在しない場合、空のファイルを作成

logging.basicConfig(
    filename=LOG_FILENAME,  # ファイル名を指定
    level=logging.DEBUG,  # 出力レベルを設定
    format="%(asctime)s - %(levelname)s - %(message)s",
)
# loggerのインスタンス化
logger = logging.getLogger(__name__)


def handle_error(error_msg):
    """
    エラーメッセージを出力し、ログに記録する関数

    Args:
    error_msg (str): エラーメッセージ

    Returns:
    None
    """
    print(f"interruption: {error_msg}")
    logger.error("interruption: %s", error_msg)


def get_jpx_data():
    """
    東証から株価データをダウンロードして取得する関数
    """

    # ダウンロードするファイルのURL
    url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # HTTPステータスコードがエラーの場合に例外を発生させる

        with open("data_j.xls", "wb") as file:
            file.write(response.content)
    except requests.exceptions.HTTPError as http_error:
        raise http_error
    except requests.RequestException as error:
        raise error


def preprocess_data(df):
    """
    ダウンロードした株価データを整形する関数

    Args:
    df (pd.DataFrame): ダウンロードした株価データが格納されたDataFrame

    Returns:
    pd.DataFrame: 整形された株価データが格納されたDataFrame
    """
    try:
        if "日付" in df.columns:
            df.drop("日付", axis=1, inplace=True)

        # 市場・商品区分に対応する文字列を辞書として定義します
        replacement_dict = {
            "プライム（内国株式）": "P",
            "スタンダード（内国株式）": "S",
            "スタンダード（外国株式）": "S",
            "グロース（内国株式）": "G",
            "グロース（外国株式）": "G",
            "PRO Market": "Pro",
            "ETF・ETN": "E",
            "REIT・ベンチャーファンド・カントリーファンド・インフラファンド": "R",
            "出資証券": "Y",
        }

        # 市場・商品区分のカラムを置換します
        df["市場・商品区分"] = df["市場・商品区分"].replace(replacement_dict)

        # 銘柄名の中身の全角英数字と全角空白を半角英数字に置換します
        df["銘柄名"] = df["銘柄名"].apply(
            lambda x: jaconv.z2h(x, kana=False, digit=True, ascii=True)
        )
        df.replace({"-": None}, inplace=True)

        # カラム名の英訳を定義します
        column_translation = {
            "コード": "code",
            "銘柄名": "name",
            "市場・商品区分": "market_product_category",
            "33業種コード": "sector33_code",
            "33業種区分": "sector33_category",
            "17業種コード": "sector17_code",
            "17業種区分": "sector17_category",
            "規模コード": "scale_code",
            "規模区分": "scale_category",
        }

        # カラム名を英訳に変更し、スネークケースに変換します
        df.rename(
            columns={
                col: column_translation.get(
                    col, col.lower().replace("・", "_").replace(" ", "_")
                )
                for col in df.columns
            },
            inplace=True,
        )

    except Exception as e:
        raise ValueError("There is no data in the DataFrame.") from e

    return df

def execute_query(db_params, query, data=None, fetch=False):
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
                    cursor.execute(query, data)
                else:
                    cursor.execute(query)
                conn.commit()
                if fetch:
                    return cursor.fetchall()
    except psycopg2.DatabaseError as error:
        conn.rollback()
        raise error


def insert_data_to_table(df, db_params):
    """
    リアルタイムの株価データをデータベースのテーブルにInsertかUpdateする関数

    Args:
    table_data (pd.DataFrame): 挿入する株価データが格納されたDataFrame
    conn (psycopg2.extensions.connection): データベースへの接続オブジェクト

    Returns:
    None
    """

    # dfのデータをmaster_stock_tableに挿入します
    insert_query = """
    INSERT INTO master_stock_table (
        code, name, market_product_category, sector33_code, sector33_category,
        sector17_code, sector17_category, scale_code, scale_category
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s
    ) ON CONFLICT (code) DO UPDATE
    SET
        name = EXCLUDED.name,
        market_product_category = EXCLUDED.market_product_category,
        sector33_code = EXCLUDED.sector33_code,
        sector33_category = EXCLUDED.sector33_category,
        sector17_code = EXCLUDED.sector17_code,
        sector17_category = EXCLUDED.sector17_category,
        scale_code = EXCLUDED.scale_code,
        scale_category = EXCLUDED.scale_category
    """

    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                for _, row in df.iterrows():
                    data = (
                        row["code"],
                        row["name"],
                        row["market_product_category"],
                        row["sector33_code"],
                        row["sector33_category"],
                        row["sector17_code"],
                        row["sector17_category"],
                        row["scale_code"],
                        row["scale_category"],
                    )
                    cursor.execute(insert_query, data)  # executemanyの代わりにexecuteを使用
                conn.commit()
    except psycopg2.DatabaseError as e:
        conn.rollback()
        raise e

    return


def parse_html_to_dataframe(html_content):
    """
    HTMLコードからIPOデータを抽出して整形する関数

    Args:
    html_content (str): 解析したいHTMLコード

    Returns:
    pd.DataFrame: 抽出・整形したIPOデータが格納されたDataFrame
    """
    # BeautifulSoupを使用してHTMLを解析
    soup = BeautifulSoup(html_content, "html.parser")

    # 2つ目のテーブルを取得
    tables = pd.read_html(str(soup), header=0)  # 1行目をヘッダーとして使用
    # 必要な列を抽出
    df = tables[1].loc[:, ["ｺｰﾄﾞ", "銘柄", "市場"]]
    # 0番目のテーブルを選択し、必要な列を抽出

    # 列名を指定して変更
    df = df.rename(
        columns={"ｺｰﾄﾞ": "code", "銘柄": "name", "市場": "market_product_category"}
    )

    # 条件に合致する行の抽出と文字列の置換
    df = df[df["market_product_category"].str.startswith("東")]

    # "市場"列の文字列から"東"を削除
    df["market_product_category"] = df["market_product_category"].str.replace(
        "東", "", regex=False
    )

    # 'name'列に"(中止)"を含まない行だけを残す
    df = df[~df["name"].str.contains("中止")]

    return df


def insert_new_rows_to_database(df, db_params):
    """
    新しいIPOデータをデータベースに挿入する関数

    Args:
    df (pd.DataFrame): 挿入するIPOデータが格納されたDataFrame
    db_params (dict): データベースへの接続情報が格納された辞書

    Returns:
    None
    """

    # 既存のデータを取得する
    select_query = "SELECT code FROM master_stock_table;"
    existing_codes = execute_query(db_params, select_query, fetch=True)
    existing_codes = [row[0] for row in existing_codes]

    # 新たに挿入する必要のある行を抽出
    new_rows_to_insert = df.loc[~df["code"].isin(existing_codes)]

    # 新たな行をmaster_stock_tableに挿入
    if not new_rows_to_insert.empty:
        insert_query = """
        INSERT INTO master_stock_table
        (code, name, market_product_category)
        VALUES (%s, %s, %s);
        """
        for row in new_rows_to_insert.itertuples(index=False):
            execute_query(db_params, insert_query, row)

def main():
    """
    メイン関数
    """

    # 開始のログを出力
    logger.info("start: %s", __name__)
    print(f"start: {__name__}")

    # データの取得
    try:
        # データを取得
        get_jpx_data()

        # ファイルパスを指定
        file_path = "data_j.xls"

        # Excelファイルを読み込む
        df = pd.read_excel(file_path)

        # ファイルを削除
        os.remove(file_path)

        # データを前処理
        df = preprocess_data(df)

        # PostgreSQLの接続情報を環境変数から取得
        db_params = {
            "host": os.environ.get("POSTGRES_HOST"),
            "database": os.environ.get("POSTGRES_DB"),
            "user": os.environ.get("POSTGRES_USER"),
            "password": os.environ.get("POSTGRES_PASSWORD"),
        }

        # データをテーブルに挿入
        insert_data_to_table(df, db_params)

        url = "https://c-eye.co.jp/ipo-list"
        html_content = requests.get(url, timeout=10).text
        df = parse_html_to_dataframe(html_content)
        insert_new_rows_to_database(df, db_params)


    except requests.exceptions.Timeout as e:
        print(f"Request timed out: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error occurred: {e}")
    except requests.exceptions.HTTPError as http_error:
        error_msg = f"An HTTP error occurred: {http_error}"
        handle_error(error_msg)
    except requests.exceptions.RequestException as request_error:
        error_msg = f"An error occurred during download: {request_error}"
        handle_error(error_msg)
    except FileNotFoundError as file_not_found:
        error_msg = f"File not found: {file_not_found}"
        handle_error(error_msg)
    except pd.errors.ParserError as parser_error:
        error_msg = f"Error parsing Excel file: {parser_error}"
        handle_error(error_msg)
    except OSError as os_error:
        error_msg = f"Error during file deletion: {os_error}"
        handle_error(error_msg)
    except ValueError as value_error:
        error_msg = f"Value error occurred: {value_error}"
        handle_error(error_msg)
    except psycopg2.DatabaseError as db_error:
        error_msg = f'An error occurred in the database: {db_error}'
        handle_error(error_msg)

    # 正常終了
    print("completion: All processes have terminated successfully.")
    logger.info("completion: All processes have terminated successfully.")

    return


if __name__ == "__main__":
    main()

# %%
