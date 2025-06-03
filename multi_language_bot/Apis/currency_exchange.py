import requests
import json

from multi_language_bot.App import API_TOKEN

res = requests.get(f'https://v6.exchangerate-api.com/v6/{API_TOKEN}/latest/USD')
res2 = requests.get(f'https://v6.exchangerate-api.com/v6/{API_TOKEN}/pair/USD/UZS')
res_json = json.loads(res.text)
res_json2 = json.loads(res2.text)

if __name__ == '__main__':
    # print(res_json)
    print(res_json2)