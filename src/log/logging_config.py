# -*- coding: utf-8 -*-
"""
このファイルは、ログの設定と関連する機能を提供します。

ファイル説明:
このファイルには、ログの設定を行う関数や、その他の機能が含まれています。
ログは、アプリケーションの実行中に発生する情報やエラーの記録に使用されます。

関数説明:
- configure_logging(log_filename): ログの設定を行う関数です。指定したログファイルにログを記録します。

"""
import os
import logging


def configure_logging(log_filename):
    """
    ログの設定を行う関数

    Args:
    log_filename (str): ログファイルの名前

    Returns:
    logging.Logger: 設定されたロガーインスタンス
    """
    if not os.path.exists(log_filename):
        open(log_filename, "w", encoding="utf-8")
    # ログの設定を行います
    logging.basicConfig(
        filename=log_filename,  # ログファイルの名前を指定
        level=logging.DEBUG,     # ログのレベルをDEBUGに設定
        format="%(asctime)s - %(levelname)s - %(message)s"  # ログのフォーマットを指定
    )
    # ロガーインスタンスを取得して返します
    logger = logging.getLogger(__name__)
    return logger
