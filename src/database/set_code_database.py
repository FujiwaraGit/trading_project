# -*- coding: utf-8 -*-
"""
このファイルは、データベースへのデータ操作を提供します。

ファイルの概要:
- select_existing_codes(db_params): データベースから既存の銘柄コードを選択する関数
- insert_rows_to_database(db_params, data): データベースに新しい行を挿入する関数
- update_rows_on_database(df, db_params): リアルタイムの株価データをデータベースのテーブルにInsertかUpdateする関数
"""

from database.db_connector import execute_query


def update_rows_on_database(db_params, df):
    """
    リアルタイムの株価データをデータベースのテーブルにInsertかUpdateする関数

    Args:
        df (pd.DataFrame): 更新する株価データが格納されたDataFrame
        db_params (dict): データベースへの接続情報が格納された辞書

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
        execute_query(db_params, insert_query, data)

    return


def select_existing_codes(db_params):
    """
    データベースから既存の銘柄コードを選択する関数

    Args:
        db_params (dict): データベースへの接続情報が格納された辞書

    Returns:
        list: 既存の銘柄コードが格納されたリスト
    """
    select_query = "SELECT code FROM master_stock_table;"
    existing_codes = execute_query(db_params, select_query, fetch=True)
    return_codes = [row[0] for row in existing_codes]
    return return_codes


def insert_rows_to_database(db_params, data):
    """
    データベースに新しい行を挿入する関数

    Args:
        db_params (dict): データベースへの接続情報が格納された辞書
        data (tuple): 挿入するデータが格納されたタプル

    Returns:
        None
    """
    insert_query = """
    INSERT INTO master_stock_table
    (code, name, market_product_category)
    VALUES (%s, %s, %s);
    """
    execute_query(db_params, insert_query, data)
