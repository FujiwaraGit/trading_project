# -*- coding: utf-8 -*-
"""
このファイルは、株価データとIPOデータの処理を行うロジックを提供します。

ファイルの概要:
- make_jpx_df(): 株価データのダウンロードから整形までの一連の処理を実行する関数
- insert_jpx_to_db(db_params, df): 株価データをデータベースに挿入する関数
- make_ipo_df(): IPOデータの抽出と整形を行う関数
- update_ipo_to_db(df, db_params): IPOデータをデータベースに更新する関数
"""

import os
import jaconv
import pandas as pd
from bs4 import BeautifulSoup
from http_requests.set_code_requests import get_jpx_data, get_ipo_data
from database.set_code_database import select_existing_codes, insert_rows_to_database, update_rows_on_database


def make_jpx_df():
    """
    株価データのダウンロードから整形までの一連の処理を実行する関数

    Returns:
        pd.DataFrame: 整形された株価データが格納されたDataFrame
    """
    # ファイルパスを指定
    file_path = "data_j.xls"
    # データの処理
    response = get_jpx_data()

    with open(file_path, "wb") as file:
        file.write(response.content)

    # Excelファイルを読み込む
    df = pd.read_excel(file_path)

    # データの前処理などの処理
    os.remove(file_path)

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

    return df


def update_jpx_to_db(df, db_params):
    """
    IPOデータをデータベースに更新する関数

    Args:
        df (pd.DataFrame): 更新するIPOデータが格納されたDataFrame
        db_params (dict): データベースへの接続情報が格納された辞書

    Returns:
        None
    """
    update_rows_on_database(df, db_params)


def make_ipo_df():
    """
    IPOデータのdfを作成する関数

    Returns:
    pd.DataFrame: 抽出・整形したIPOデータが格納されたDataFrame
    """
    response = get_ipo_data()
    html_content = response.text

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


def insert_ipo_to_db(db_params, df):
    """
    株価データをデータベースに挿入する関数

    Args:
        db_params (dict): データベースへの接続情報が格納された辞書
        df (pd.DataFrame): 挿入する株価データが格納されたDataFrame

    Returns:
        None
    """
    existing_codes = select_existing_codes(db_params)

    new_rows_to_insert = df.loc[~df["code"].isin(existing_codes)]

    if not new_rows_to_insert.empty:
        for _, row in new_rows_to_insert.iterrows():
            data = (row["code"], row["name"], row["market_product_category"])
            insert_rows_to_database(db_params, data)
