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
