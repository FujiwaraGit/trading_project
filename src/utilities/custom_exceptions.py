class MissingAPIIdError(Exception):
    """
    API IDが指定されていないときに発生する例外クラス
    """
    pass


class NoMatchingCodeError(Exception):
    """
    対応するコードが存在しないときに発生する例外クラス
    """
    pass
