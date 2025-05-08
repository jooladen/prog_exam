
import pandas as pd
import time
import requests


import hashlib
import hmac
import base64

class Signature:

    @staticmethod
    def generate(timestamp, method, uri, secret_key):
        message = "{}.{}.{}".format(timestamp, method, uri)
        hash = hmac.new(bytes(secret_key, "utf-8"), bytes(message, "utf-8"), hashlib.sha256)

        hash.hexdigest()
        return base64.b64encode(hash.digest())


def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = Signature.generate(timestamp, method, uri, secret_key)
    
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 
            'X-API-KEY': api_key, 'X-Customer': str(customer_id), 'X-Signature': signature}


def getresults(hintKeywords):
    print(hintKeywords)
    print(1)
    BASE_URL = 'https://api.searchad.naver.com'
    API_KEY = '0100000000c6d85b711847dd9cc75fd8a871b12eb61c9d23bf8aa12e998a6eb618b77ffd55'
    SECRET_KEY = 'AQAAAACUIl5duGI+KnLo1dWvs+hThAJz7k28wJRLE+XUuy3/KQ=='
    #SECRET_KEY = 'lbJwq0cr3d'
    CUSTOMER_ID = '3455835'
    #CUSTOMER_ID = 'OOOwOkFmGACcqwV269OU'

    uri = '/keywordstool'
    method = 'GET'

    params={}

    params['hintKeywords']=hintKeywords
    params['showDetail']=1
    print('start')
    r=requests.get(BASE_URL + uri, params=params, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
    print('end')
    print("r >>> ", r)

    return pd.DataFrame(r.json()['keywordList'])

if __name__ == '__main__':
    print(0)
    #df = getresults('chatgpt')
    df = getresults('CHATGPT')
    if not df.empty:
        print(df[['relKeyword', 'monthlyPcQcCnt', 'monthlyMobileQcCnt', 'compIdx']])