from re import compile, sub, escape
from string import punctuation
from flask_restful import Api, Resource
from flask import Flask
from pymorphy2 import MorphAnalyzer
import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords
import pandas as pd
import logging
import sys



app = Flask(__name__)
api = Api(app)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


class Bot_Answer(Resource):
    def get(self, user_answer):
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
                return 'RZH', 200

        for word in stem_answer_list:
            if '1' in stem_answer_list and word in data[1][1]:
                return 'RZH', 200

        for word in stem_answer_list:
            if '1' in stem_answer_list and word in data[1][0]:
                return 'RZH', 200

        for word in stem_answer_list:
            if '2' in stem_answer_list and word in data[2][1]:
                return 'RZH', 200
        for word in stem_answer_list:
            if '2' in stem_answer_list and word in data[2][2]:
                return 'RZH', 200

        for word in stem_answer_list:
            if '2' in stem_answer_list and word in data[2][0]:
                return 'RZH', 200
        return 'RZH', 404


api.add_resource(Bot_Answer, '/get_answer/<string:user_answer>')
if __name__ == '__main__':
    app.run(debug=True)
