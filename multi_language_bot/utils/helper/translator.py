import json

from multi_language_bot.App import BASE_DIR
from multi_language_bot.utils.db.postgres_db import pg


def google_translate(chat_id):
    lang = pg.get_lang(chat_id)
    with open(f'{BASE_DIR}/locals/{lang}/data.json', 'rb') as file:
        datas = json.load(file)
    return datas


if __name__ == '__main__':
    # datas = google_translate(432472837)
    # print(datas['start'])


   fayl=  [
    [26,
      2,
      "9-sinf"
    ],
    [33,
      3,
      "11-sinf"
    ],
    [ 3,
      3,
      "1-sinf"
    ],
    [5,
      2,
      "2-sinf"
    ],
    [27,
      3,
      "9-sinf"
    ],
    [23,
      2,
      "8-sinf"
    ],
    [15,
      3,
      "5-sinf"
    ],
    [22,
      1,
      "8-sinf"
    ],
    [1,
      1,
      "1-sinf"
    ],
    [20,
      2,
      "7-sinf"
    ],
    [8,
      2,
      "3-sinf"
    ],
    [4,
      1,
      "2-sinf"
    ],
    [18,
      3,
      "6-sinf"
    ],
   [31,
      1,
      "11-sinf"
    ],
    [6,
      3,
      "2-sinf"
    ],
    [21,
      3,
      "7-sinf"
    ],
    [28,
      1,
      "10-sinf"
    ],
    [19,
      1,
      "7-sinf"
    ],
    [13,
      1,
      "5-sinf"
    ],
    [24,
      3,
      "8-sinf"
    ],
    [ 12,
      3,
      "4-sinf"
    ],
    [29,
      2,
      "10-sinf"
    ],
    [30,
      3,
      "10-sinf"
    ],
    [16,
      1,
      "6-sinf"
    ],
    [25,
      1,
      "9-sinf"
    ],
    [ 17,
      2,
      "6-sinf"
    ],
    [14,
      2,
      "5-class"
    ],
    [2,
      2,
      "1-class"
    ],
    [10,
      1,
      "4-class"
    ],
    [7,
      1,
      "3-class"
    ],
    [32,
      2,
      "11-class"
    ],
    [ 11,
      2,
      "4-class"
    ],
    [9,
      3,
      "3-class"
    ]
  ]

   print(len(fayl))