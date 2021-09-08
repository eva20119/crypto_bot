from datetime import datetime
import requests
import time
import json

ID = "389449011" #eve
# ID = "1350155390" #me
TOKEN = "1892699845:AAGcnCe2THyhoQLvgLs84VFXV9p1zV_AcHg"
PASS_TIME = 10
GAS_LIMIT = 30

def sendText(text):
    payload = {
        'chat_id': ID,
        'text': text
    }
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data = payload)

def fetchEtherscanGas():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    }
    cookies = {
        "__cflb": "02DiuFnsSsHWYH8WqVXaqGvd6BSBaXQLUEZRvKiFMHEo6",
        "_ga": "GA1.2.28964803.1623813105",
        "_gid": "GA1.2.1624046306.1623813105",
        "__cf_bm": "2d46c6b7d0f5edfc99709666419abb44f3feaf50-1623813106-1800-AVd0cUzxe4OCp5YsguYhNpv0KoF4zSNmDpI4G/5dC7EEkLKZ3LpaNzCboqaM0Ed9HDeeWkPKGu5jW/rXr9S5rwK0rZaLQs61F+zl5ZEZHkqv/jCipK3HfsBEn8YKJf+i9w==",
        "ASP.NET_SessionId": "e5s5jesudkxfihkp1dnf0dv1",
        "_gat_gtag_UA_46998878_6": "1",
    }
    s = requests.Session()

    res = s.get('https://etherscan.io/autoUpdateGasTracker.ashx?sid=39accb547d8ff04abbb5a7e6c2e0a6fe', headers=headers, cookies=cookies)
    json = res.json();
    lowPrice = json["lowPrice"]
    avgPrice = json["avgPrice"]
    highPrice = json["highPrice"]
    print(f'Low: {lowPrice}')
    print(f'Average: {avgPrice}')
    print(f'High: {highPrice}')

    return {
        "lowPrice": lowPrice,
        "avgPrice": avgPrice,
        "highPrice": highPrice
    }

def receiveText():
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    res = requests.get(url)
    result = res.json()['result']
    text = result[-1]['message']['text']
    if text == 'gas':
        gas = fetchEtherscanGas()
        lowPrice = gas["lowPrice"]
        avgPrice = gas["avgPrice"]
        highPrice = gas["highPrice"]
        sendText(f'Low: {lowPrice}\nAverage: {avgPrice}\nHigh: {highPrice}')
    elif text.startswith("ipfs"):
        url = f"https://ipfs.io/ipfs/{text.split('//')[1]}"

        metadata = requests.get(url).json()
        message = ""
        message += f"image: https://ipfs.io/ipfs/{metadata['image'].split('//')[1]}\n"
        attributes = metadata.get('attributes') or []

        for i in attributes:
            message += f"{i.get('trait_type')}: {i.get('value')}\n"
        sendText(message)

receiveText()
