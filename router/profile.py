from flask import Flask, jsonify, request, render_template
import jwt
from flask import Blueprint
from werkzeug.utils import secure_filename
from datetime import datetime
import certifi
import jwt

SECRET_KEY = '$lucky7'

# DB 연결 코드
from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://luckyseven:luckyseven@cluster0.2hyld.mongodb.net/myFirstDatabase?retryWrites=true&w=majority',
    tlsCAFile=certifi.where())
db = client.od_project

bp = Blueprint("profile", __name__, url_prefix="/profile")


@bp.route('/', methods=['GET'])
def profile():
    # token_receive = request.cookies.get('mytoken')
    # payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

    user_info = db.USER.find_one({"id": 'jaehyun'})  # id, num, nickname, feed_images, content, like, reply
    print(user_info)
    results = sorted(list(db.result.find({'company': user_info['company']})), key=lambda x: x['date'], reverse=True)
    print(results)

    for i, res in enumerate(results):
        results[i]['predict_path'] = '../' + str(res['predict_path'])
        print(results[i]['predict_path'])


    return render_template('profile.html', user_info=user_info, results = results)
