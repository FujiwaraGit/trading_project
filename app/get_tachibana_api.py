# %%
"""
立花証券のAPIを使用して株式データを取得するPythonプログラムです。

使用方法:

自分のユーザーID、パスワード、第2パスワードを変数に設定してください。
CODE_LISTに取得したい株式の銘柄コードをリストとして追加してください。
プログラムを実行してください。
注意事項:

ログインが成功した場合、株式データを取得します。
応答データはJSON形式で返されます。
ログインに成功した場合、応答データには取得した株式データが含まれます。
"""

import datetime
import json
import pytz
import urllib3


class ClassTachibanaAccount:
    """
    立花証券口座クラス

    Attributes:
    json_fmt (str): 応答データのフォーマット指定
    url_base (str): ログイン先のURL
    user_id (str): ユーザーID
    password (str): パスワード
    password_sec (str): 第2パスワード
    request_url (str): request用仮想URL
    event_url (str): event用仮想URL
    tax_category (str): 譲渡益課税区分（1：特定 3：一般 5：NISA）

    Methods:
        set_property(request_url, event_url, tax_category):
            プロパティを設定するメソッド
    """

    def __init__(self, json_fmt, url_base, user_id, password, password_sec):
        """
        立花証券口座クラスのコンストラクタ

        Args:
            json_fmt (str): 応答データのフォーマット指定
            url_base (str): ログイン先のURL
            user_id (str): ユーザーID
            password (str): パスワード
            password_sec (str): 第2パスワード
        """
        self.int_p_no = 0  # request通番
        self.json_fmt = "5"
        self.url_base = url_base
        self.user_id = user_id
        self.password = password
        self.password_sec = password_sec
        self.request_url = ""
        self.event_url = ""
        self.tax_category = ""

    def set_property(self, request_url, event_url, tax_category):
        """
        プロパティを設定するメソッド

        Args:
            request_url (str): request用仮想URL
            event_url (str): event用仮想URL
            tax_category (str): 譲渡益課税区分（1：特定 3：一般 5：NISA）
        """
        self.request_url = request_url
        self.event_url = event_url
        self.tax_category = tax_category


def func_check_json_dquat(str_value):
    """
    JSONの値の前後にダブルクオーテーションがない場合に付ける関数

    Args:
        str_value (str): チェック対象の文字列

    Returns:
        str: 前後にダブルクオーテーションが付けられた文字列
    """
    if len(str_value) == 0:
        str_value = '""'

    if not str_value[:1] == '"':
        str_value = '"' + str_value

    if not str_value[-1:] == '"':
        str_value = str_value + '"'
    return str_value


def func_p_sd_date(int_systime):
    """
    "p_sd_date"の書式の文字列としてシステム時刻を返す関数

    Args:
        int_systime (datetime): システム時刻を表すdatetimeオブジェクト

    Returns:
        str: "p_sd_date"の書式の文字列としてフォーマットされたシステム時刻
    """
    str_psddate = ""
    str_psddate = str_psddate + str(int_systime.year)
    str_psddate = str_psddate + "." + ("00" + str(int_systime.month))[-2:]
    str_psddate = str_psddate + "." + ("00" + str(int_systime.day))[-2:]
    str_psddate = str_psddate + "-" + ("00" + str(int_systime.hour))[-2:]
    str_psddate = str_psddate + ":" + ("00" + str(int_systime.minute))[-2:]
    str_psddate = str_psddate + ":" + ("00" + str(int_systime.second))[-2:]
    str_psddate = (
        str_psddate + "." + (("000000" + str(int_systime.microsecond))[-6:])[:3]
    )
    return str_psddate


def func_make_url_request(auth_flg, url_target, tachibana_account, req_item_list):
    """
    requestの文字列を作成して返す関数

    Args:
        auth_flg (bool): 認証フラグ
        url_target (str): ターゲットURL
        tachibana_account (TachibanaAccount): tachiban口座属性クラスのインスタンス
        req_item_list (list): request項目が格納されているリスト

    Returns:
        str: 作成されたrequestの文字列
    """
    tachibana_account.int_p_no += 1  # request通番をカウントアップ
    str_p_sd_date = func_p_sd_date(
        datetime.datetime.now(pytz.timezone("Asia/Tokyo"))
    )  # システム時刻を所定の書式で取得
    work_url = url_target
    if auth_flg is True:
        work_url = work_url + "auth/"
    work_url = work_url + "?{"
    work_url = (
        work_url
        + '"p_no":'
        + func_check_json_dquat(str(tachibana_account.int_p_no))
        + ","
    )
    work_url = work_url + '"p_sd_date":' + func_check_json_dquat(str_p_sd_date) + ","

    for item in req_item_list:
        if len(item["key"]) > 0:
            work_url += item["key"] + ":" + func_check_json_dquat(str(item["value"])) + ","
    work_url = work_url[:-2] + '"}'
    return work_url


def func_login(tachibana_account):
    """
    ログインを行い、応答データを返す関数

    Args:
        tachibana_account (TachibanaAccount): 立花証券口座属性クラスのインスタンス

    Returns:
        json: 応答データのjson型
    """
    http = urllib3.PoolManager()
    req_item_list = [
        {"key": '"sCLMID"', "value": "CLMAuthLoginRequest"},
        {"key": '"sUserId"', "value": tachibana_account.user_id},
        {"key": '"sPassword"', "value": tachibana_account.password},
        {"key": '"sJsonOfmt"', "value": tachibana_account.json_fmt},
    ]

    work_url = func_make_url_request(
        True, tachibana_account.url_base, tachibana_account, req_item_list
    )

    print(work_url)

    req = http.request("GET", work_url)
    bytes_reqdata = req.data
    str_shiftjis = bytes_reqdata.decode("shift-jis", errors="ignore")
    json_req = json.loads(str_shiftjis)

    return json_req


async def func_get_stock_data(tachibana_account, code_list, client):
    """
    リアルタイムの株価データを取得する関数

    Args:
    tachibana_account (TachibanaAccount): 立花証券口座属性クラスのインスタンス
    code_list (list): 株価データを取得する銘柄コードのリスト

    Returns:
        json: 取得した株価データの辞書型
    """

    req_item_list = [
        {"key": '"sCLMID"', "value": '"CLMMfdsGetMarketPrice"'},
        {"key": '"sTargetIssueCode"', "value": ",".join(map(str, code_list))},
        {
            "key": '"sTargetColumn"',
            "value": (
                # 現値,出来高,前日終値,始値,高値,安値,VWAP
                "pDPP,pDV,pPRP,pDOP,pDHP,pDLP,pVWAP,"
                # 売気配値,売気配値種,買気配値,買気配値種
                "pQAP,pQAS,pQBP,pQBS"
                # 成売,成買,OVER,UNDER"
                "pAAV,pABV,pQOV,pQUV"
                # 売値10,売値9,売値8,売値7,売値6,売値5,売値4,売値3,売値2,売値1
                "pGAP10,pGAP9,pGAP8,pGAP7,pGAP6,pGAP5,pGAP4,pGAP3,pGAP2,pGAP1,"
                # 買値10,買値9,買値8,買値7,買値6,買値5,買値4,買値3,買値2,買値1
                "pGBP10,pGBP9,pGBP8,pGBP7,pGBP6,pGBP5,pGBP4,pGBP3,pGBP2,pGBP1,"
                # 売量10,売量9,売量8,売量7,売量6,売量5,売量4,売量3,売量2,売量1
                "pGAV10,pGAV9,pGAV8,pGAV7,pGAV6,pGAV5,pGAV4,pGAV3,pGAV2,pGAV1,"
                # 買量10,買量9,買量8,買量7,買量6,買量5,買量4,買量3,買量2,買量1
                "pGBV10,pGBV9,pGBV8,pGBV7,pGBV6,pGBV5,pGBV4,pGBV3,pGBV2,pGBV1"
            ),
        },
        {"key": '"sJsonOfmt"', "value": tachibana_account.json_fmt},
    ]

    work_url = func_make_url_request(
        False, tachibana_account.request_url, tachibana_account, req_item_list
    )

    response = await client.get(work_url)
    response.raise_for_status()  # ステータスコードがエラーであれば例外を発生させる
    data = response.content
    json_data = json.loads(data.decode("shift-jis", errors="ignore"))

    return json_data

# %%