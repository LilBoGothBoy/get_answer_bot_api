from flask_restful import Api, Resource
from pymorphy2 import MorphAnalyzer
from re import compile, sub, escape
from flask import Flask, request
from string import punctuation
import pandas as pd
import logging
import json
import sys
import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords


app = Flask(__name__)
api = Api(app)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


class Bot_Answer(Resource):
    def post(self):
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            json_object = request.json
            json_object = json.loads(json_object)
            user_answer = json_object['Text'] + " " + json_object['Project']
            print(user_answer)
            data = pd.read_excel('data.xlsx')
            stop_words = stopwords.words('russian')
            user_answer = compile('<.*?>').sub('', user_answer)
            user_answer = compile('[%s]' % escape(
                punctuation)).sub(' ', user_answer)
            user_answer = sub('\s+', ' ', user_answer)
            user_answer = sub(r'[^\w\s]', '', str(user_answer))
            user_answer = sub(r'\s+', ' ', user_answer)
            morph = MorphAnalyzer()
            stem_answer_list = [morph.parse(
                word)[0].normal_form for word in user_answer.split()]

            for word in stem_answer_list:
                if word in stop_words:
                    del stem_answer_list[stem_answer_list.index(word)]
            for word in stem_answer_list:
                if '1' in stem_answer_list and word in data[1][2]:
                    return 'РЖД. Техническая поддержка.', 200

            for word in stem_answer_list:
                if '1' in stem_answer_list and word in data[1][1]:
                    return 'РЖД. Скидки и акции.', 200

            for word in stem_answer_list:
                if '1' in stem_answer_list and word in data[1][0]:
                    return 'РЖД. Билеты и расписание. ', 200

            for word in stem_answer_list:
                if '2' in stem_answer_list and word in data[2][1]:
                    return 'СБЕР. Условия доставки.', 200
            for word in stem_answer_list:
                if '2' in stem_answer_list and word in data[2][2]:
                    return 'СБЕР. Оформление заказа.', 200

            for word in stem_answer_list:
                if '2' in stem_answer_list and word in data[2][0]:
                    return 'СБЕР. Оформление заказа.', 200
            return 'Совпадений не найдено!', 404
        else:
            return 'Content-Type not supported!'


api.add_resource(Bot_Answer, '/get_answer')
if __name__ == '__main__':
    app.run(debug=True)
