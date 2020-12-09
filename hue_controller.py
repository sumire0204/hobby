# -*- coding: utf-8 -*-

import requests
import configparser

# 環境変数の読み込み 
config = configparser.ConfigParser()
config.read('setting.ini')
IP_ADDRESS = config['development']['ip_address']
USERNAME = config['development']['username']

def request2hue():
    """ hueのstateを変更する
    """
    # stateを取得
    HUE_API = f"http://{IP_ADDRESS}/api/{USERNAME}/groups"
    res = requests.get(HUE_API)
    jsonData = res.json()
    state = jsonData["1"]["action"]["on"]

    # stateを変更
    if state == False:
        requests.put(HUE_API + "/1/action", json = {"on":True, "bri":128, "xy":[0.48, 0.41]})
        print("turn on")

    if state == True:
        requests.put(HUE_API + "/1/action", json = {"on":False})
        print("turn off")

if __name__ == "__main__":
    request2hue()