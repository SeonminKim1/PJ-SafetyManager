from flask import Flask, jsonify, request, render_template, redirect, url_for
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
    token_receive = request.cookies.get('mytoken')
    print('token_receive', token_receive)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        user_info = db.USER.find_one({"id": payload['id']})  # id, num, nickname, feed_images, content, like, reply
        print(user_info)
        results = sorted(list(db.RESULT.find({'company': user_info['company']})), key=lambda x: x['date'], reverse=True)
        print(results)

        for i, res in enumerate(results):
            results[i]['upload_path'] = '../' + str(res['upload_path'])
            results[i]['predict_path'] = '../' + str(res['predict_path'])

        return render_template('profile.html', user_info=user_info, results=results)

    except jwt.ExpiredSignatureError:  # 해당 token의 로그인 시간이 만료시 login 페이지로 redirect
        return redirect(url_for("user.login"))
    except jwt.exceptions.DecodeError:  # 해당 token이 다르다면 login 페이지로 redirect
        return redirect(url_for("user.login"))
