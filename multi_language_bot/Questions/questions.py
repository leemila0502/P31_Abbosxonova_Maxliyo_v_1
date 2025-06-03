from os import getenv
from collections import  defaultdict
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv

load_dotenv()

class Questions:
    def __init__(self):

        self.connect = psycopg2.connect(
            dbname=getenv('DB_NAME2'),
            user=getenv('USER2'),
            password=getenv('PASSWORD2'),
            host=getenv('HOST2'),
            port=getenv('PORT2')
        )
        self.cursor = self.connect.cursor(cursor_factory=DictCursor)

    def execute(self, query):
        with self.connect:
            self.cursor.execute(query)
            return self.cursor

    def fetchall(self, query):
        cursor = self.execute(query)
        results=cursor.fetchall()
        return [(dict(rows)) for rows in results]

    def category(self):
        query = """SELECT category.id,category.name FROM category ORDER BY category.id """
        return self.fetchall(query)

    def subcategory(self):
        query=f"""SELECT DISTINCT subcategory.id , subcategory.category_id,subcategory.name FROM subcategory join category on category.id=subcategory.category_id """
        return self.fetchall(query)

    def get_question(self,category_id):
        query = f"""
        SELECT
    category.id AS category_id,
    category.name AS category_name,

    subcategory.id AS subcat_id,
    subcategory.name AS subcat_name,

    quiz.id AS quiz_id,
    quiz.question,

    option.id AS option_id,
    option.option_text,
    option.is_correct

FROM category
JOIN subcategory ON subcategory.category_id = category.id
JOIN quiz ON quiz.subcategory_id = subcategory.id
JOIN option ON option.quiz_id = quiz.id
WHERE category.id = {category_id} 
ORDER BY subcat_id, quiz_id, option_id;
        """
        return self.fetchall(query)

    def format(self,results):
        data = defaultdict(lambda:defaultdict(lambda:defaultdict(list)))
        for row in results:
            category = row['category_name']
            subcategory=row['subcat_name']
            question=row['question']
            option={
               'option_id': row['option_id'],
            'option_text': row['option_text'],
            'is_correct': row['is_correct']
            }
            data[category][subcategory][question].append(option)

        return data
    def convert(self,obj):
        if isinstance(obj,defaultdict):
            return {k: self.convert(v) for k,v in obj.items()}
        elif isinstance(obj,dict):
            return {k: self.convert(v) for k, v in obj.items()}
        elif isinstance(obj,list):
            return  [self.convert(i) for i in obj]
        else:
            return obj

if __name__ == "__main__":
    ques = Questions()
    # print(ques.category())
    print(ques.subcategory())
    # questions=ques.get_question(9)
    # dat=ques.convert(ques.format(questions))
    # from pprint import pprint
    # pprint(dat)
    # import json
    # with open('C:/Users/user/PycharmProjects/P31_Abbosxonova_Maxliyo_v_1/multi_language_bot/locals/uz/data.json','r',encoding="utf-8") as file:
    #     existing=json.load(file)
    # existing.update(dat)
    # with open('C:/Users/user/PycharmProjects/P31_Abbosxonova_Maxliyo_v_1/multi_language_bot/locals/uz/data.json', "w", encoding="utf-8") as file:
    #     json.dump(existing, file, ensure_ascii=False, indent=4)




