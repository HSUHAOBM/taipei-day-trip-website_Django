import requests

import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')
parent_dir = os.path.dirname(os.path.abspath(__file__))
config.read(parent_dir + "/config.ini")

partnerkey = config.get('tappay', 'partner_key')
# print("partnerkey",partnerkey)
# partnerkey = '111111111111'





url="https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
def paybyprime(data):
    paybyprimedata={}

    paybyprimedata={
    "partner_key":partnerkey,
    "prime": data["prime"],
    "amount": data["order"]["price"],
    "merchant_id": "hao66bmbm_ESUN",
    "details": "TapPay Test",
    "cardholder": {
        "phone_number":data["order"]["contact"]["phone"],
        "name":data["order"]["contact"]["name"],
        "email":data["order"]["contact"]["email"],
        "zip_code": "100",
        "address": "台北市天龍區芝麻街1號1樓",
        "national_id": "A123456789"
        }
    }
    print("paybyprimedata",paybyprimedata)

    my_headers = {
        "Content-Type": "application/json",
        "x-api-key": partnerkey
        }

    r = requests.post(url, headers = my_headers,json=paybyprimedata)
    print(r.status_code)
    print(r.json())
    return r.json()