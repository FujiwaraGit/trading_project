# %%
import os
from get_tachibana_api import ClassTachibanaAccount, func_login

URL_BASE = "https://demo-kabuka.e-shiten.jp/e_api_v4r3/"
MY_USERID = os.environ.get('TACHIBANA_USERID')
MY_PASSWORD = os.environ.get('TACHIBANA_PASSWORD')
MY_PASSWORD2 = os.environ.get('TACHIBANA_PASSWORD2')
CODE_LIST = ["5240", "9227", "3697", "5129"]


tachibana_account = ClassTachibanaAccount(
    json_fmt='"2"',
    url_base=URL_BASE,
    user_id=MY_USERID,
    password=MY_PASSWORD,
    password_sec=MY_PASSWORD2,
)  # 立花証券口座インスタンス
#%%
json_response = func_login(tachibana_account)  # ログイン処理を実施


# 取得した値を口座属性クラスに設定
tachibana_account.set_property(
    request_url=json_response.get("sUrlRequest"),
    event_url=json_response.get("sUrlEvent"),
    tax_category=json_response.get("sZyoutoekiKazeiC"),
)

# %%

json_response

# %%
