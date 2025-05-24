import requests
import json
from multi_language_bot.App import TOKEN

res=requests.get(f'https://api.telegram.org/bot{TOKEN}/getMe')
res_json=json.loads(res.text)

print(res_json)