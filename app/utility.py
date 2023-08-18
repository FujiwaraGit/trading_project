"""
ユーティリティ関数のプログラム

このプログラムは、異なる用途で使用される便利なユーティリティ関数を提供します。
以下の関数が実装されています。
- 空文字列をNoneに変換する関数: 空文字列を含む辞書を受け取り、空文字列をNoneに変換します。
- 現在の時刻が15時を過ぎているかを判定する関数: 現在のエポック秒を受け取り、現在の時刻が15時を過ぎているかを判定します。
- 指定された日付が東証の休日かどうかを判定する関数: 日付を受け取り、指定された日付が東証の休日かどうかを判定します。
- 今日が東証の休日かどうかを判定する関数: 今日の日付を取得し、今日が東証の休日かどうかを判定します。

実行方法:
プログラムの実行はmain関数を呼び出すことで行います。
main関数内で各ユーティリティ関数の使用例が示されています。

注意:
本プログラムはあくまでサンプルとして提供されるものであり、実際の運用にはさらなる検証や適応が必要です。
各関数の使用にあたっては適切な引数を指定し、返り値の結果を適切に利用してください。
"""

# %%
import datetime
import subprocess
import urllib.parse
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
    jpx_holidays = holidays.JP(years=datetime.date.today().year)

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


def func_execute_curl_command(url):
    """
    指定されたURLに対してcurlコマンドを実行し、結果を返す関数です。

    Args:
        url (str): 実行するURL。

    Returns:
        result(str): 実行結果
        成功時は'stdout'
        失敗時は'stderr'
    """
    # URLからパラメータ部分を抽出
    params_start = url.find('?')
    base_url = url[:params_start]
    params = url[params_start+1:]

    # パラメータをURLエンコード
    encoded_params = urllib.parse.quote(params, safe='')

    # 最終的なフォーマットに整形
    formatted_url = f'{base_url}?{encoded_params}'

    # curlコマンドを組み立て
    curl_command = f'curl -s -k -X GET {formatted_url}'

    # curlコマンドを実行
    result = subprocess.run(curl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        return result.stdout
    else:
        raise Exception(result.stderr)
# %%
