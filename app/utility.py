def convert_empty_string_to_none(item):
    """
    空文字列をNoneに変換する関数

    Args:
    item (dict): 空文字列を含む辞書

    Returns:
    dict: 空文字列がNoneに変換された辞書
    """
    converted_item = {}
    for key, value in item.items():
        if value == '':
            converted_item[key] = None
        else:
            converted_item[key] = value
    return converted_item


def is_after_15_oclock(current_epoch_time):
    """
    現在の時刻が15時を過ぎているかを判定する関数

    Args:
        current_epoch_time (float): 現在のエポック秒

    Returns:
        bool: 現在の時刻が15時を過ぎている場合はTrue、それ以外はFalse
    """
    current_jst_time = current_epoch_time + 9 * 3600
    current_hour = int(current_jst_time / 3600) % 24
    return current_hour >= 15
