# coding:utf-8
import pymongo

__author__ = 'lyb'
# Date:2018/8/9 17:00

from flask import Flask, render_template, g, request, redirect, url_for
import sys
from config import FLASK_BASE_DIR
sys.path.append(FLASK_BASE_DIR)
from longzu5.settings import MONGO_TABLE, MONGO_URI, MONGO_DB


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/article/<int:number>', methods=('GET', 'POST'))
def show_article(number):
    neir = find_in_mongo(number)[0]
    return render_template('article.html', neir=neir, number=number)

@app.route('/jump', methods=("POST",))
def jump_to_page():
    number = int(request.form['page'])
    neir, article = find_in_mongo(number)
    if number > article.count():
        return render_template('article.html', error='错误，超出章节数')
    else:
        neir = article.find_one({"number": number})
        return render_template('article.html', neir=neir, number=number)

def find_in_mongo(number):
    client = pymongo.MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    article = db.get_collection(MONGO_TABLE)
    neir = article.find_one({"number": number})
    return neir, article


if __name__ == '__main__':
    app.run()
