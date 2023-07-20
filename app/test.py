#%%
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl
import requests

#%%
class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,maxsize=maxsize,block=block,ssl_version=ssl.PROTOCOL_TLSv1)

s = requests.Session()
s.mount('https://', MyAdapter())

url = 'https://demo-kabuka.e-shiten.jp/e_api_v4r3/auth/?{"p_no":"1","p_sd_date":"2023.06.27-01:35:11.923","sCLMID":"CLMAuthLoginRequest","sUserId":"fps04170","sPassword":"1997805d","sJsonOfmt":"5"}'
r = s.get(url)
# %%

# %%
import urllib3
import ssl
sess = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries = 20)
sess.mount('http://', adapter)
# %%

# %%
from urllib.request import urlopen
urlopen(url, context=ssl._create_unverified_context()).read()

# %%
