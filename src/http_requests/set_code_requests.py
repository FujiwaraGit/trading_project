# -*- coding: utf-8 -*-
"""
このファイルは、株価データおよびIPOデータを取得するためのリクエストを送信する関数を提供します。

ファイルの概要:
- get_jpx_data(): 東証から株価データをダウンロードして取得する関数
- get_ipo_data(): 指定されたURLからHTMLコードを取得する関数
"""
import requests


def get_jpx_data():
    """
    東証から株価データをダウンロードして取得する関数

    Returns:
        None
    Raises:
        requests.exceptions.HTTPError: HTTPエラーが発生した場合
        requests.RequestException: リクエストエラーが発生した場合
    """

    # ダウンロードするファイルのURL
    url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # HTTPステータスコードがエラーの場合に例外を発生させる

    except requests.exceptions.HTTPError as http_error:
        raise http_error
    except requests.RequestException as error:
        raise error

    return response


def get_ipo_data():
    """
    指定されたURLからHTMLコードを取得する関数

    Args:
    url (str): 取得したいウェブページのURL

    Returns:
    str: 取得したHTMLコード
    """
    url = "https://c-eye.co.jp/ipo-list"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # エラーレスポンスを検出
    except requests.exceptions.RequestException as e:
        raise e

    return response
