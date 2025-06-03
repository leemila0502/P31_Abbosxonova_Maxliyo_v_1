import json

from multi_language_bot.App import BASE_DIR


class Functions:
    def categories(self,lang):
        with open(f'{BASE_DIR}/locals/{lang}/data.json', 'rb') as file:
            datas = json.load(file)
            data = datas["category"]
        return data

    def subcategories(self,lang):
        with open(f'{BASE_DIR}/locals/{lang}/data.json', 'rb') as file:
            datas = json.load(file)
            data = datas["subcategory"]
        return data


    def get_quizzes(self,cat_name,sub_name,lang):
        with open(f'{BASE_DIR}/locals/{lang}/data.json', 'rb') as file:
            datas = json.load(file)
            data = datas["quizzes"][f"{cat_name}"][f"{sub_name}"]
        return data



    def categoriesa(self,lang,catid):
        with open(f'{BASE_DIR}/locals/{lang}/data.json', 'rb') as file:
            datas = json.load(file)
            data = datas["category"]
            for d in data:
                if d[0]==catid:
                    p=d[1]
            return p


    def subcategoriesa(self,lang,catid,sub_id):
        with open(f'{BASE_DIR}/locals/{lang}/data.json', 'rb') as file:
            datas = json.load(file)
            data = datas["subcategory"]
            for d in data:
                if d[0]==sub_id and d[1]==catid:
                  return d[0]










if __name__=='__main__':
    f=Functions()
    # print(f.subcategories(1))

