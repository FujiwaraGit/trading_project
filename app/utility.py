# %%
import datetime
import holidays


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


def is_holiday_jpx(date):
    """
    指定された日付が東証の休日かどうかを判定する関数

    Args:
    date (str or datetime.date): 判定したい日付。文字列またはdatetime.dateオブジェクトで指定します。

    Returns:
    bool: 休日であればTrue、休日でなければFalseを返します。
    """
    # 東証の休日カレンダーを取得
    jpx_holidays = holidays.Japan(years=datetime.date.today().year)

    # 祝日として1月2日、1月3日、12月31日を追加
    jpx_holidays.append({datetime.date(datetime.date.today().year, 1, 2): "2nd January"})
    jpx_holidays.append({datetime.date(datetime.date.today().year, 1, 3): "3rd January"})
    jpx_holidays.append({datetime.date(datetime.date.today().year, 12, 31): "31st December"})

    # dateが文字列の場合はdatetime.dateオブジェクトに変換
    if isinstance(date, str):
        try:
            date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Invalid date format. Please use 'YYYY-MM-DD' format.")

    # 判定
    return date in jpx_holidays or date.weekday() >= 5  # 土曜日(5)か日曜日(6)であれば休日とみなす


def is_today_holiday():
    """
    今日が東証の休日かどうかを判定する関数

    Returns:
    bool: 今日が休日であればTrue、休日でなければFalseを返します。
    """
    # 今日の日付を取得
    today = datetime.date.today()

    # 今日が東証の休日か否かを判定
    is_holiday_today = is_holiday_jpx(today)

    return is_holiday_today


# %%
