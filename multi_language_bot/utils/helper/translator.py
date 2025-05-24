import json

from multi_language_bot.App import BASE_DIR
from multi_language_bot.utils.db.postgres_db import pg


def google_translate(chat_id):
    lang = pg.get_lang(chat_id)
    with open(f'{BASE_DIR}/locals/{lang}/data.json', 'rb') as file:
        datas = json.load(file)
    return datas


if __name__ == '__main__':
    datas = google_translate(432472837)
    print(datas['start'])

