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

        page = request.args.get('page', type=int, default=1)  # 페이지

        results = sorted(list(db.RESULT.find({'company': user_info['company']}).skip((page-1)*10).limit(10)), key=lambda x: x['date'], reverse=True)
        print(results)

        for i, res in enumerate(results):
            results[i]['upload_path'] = '../' + str(res['upload_path'])
            results[i]['predict_path'] = '../' + str(res['predict_path'])

        per_page = 10
        page_block = 1
        start_page = int((page - 1) / page_block * page_block + 1)
        end_page = start_page + page_block - 1
        count = len(list(db.RESULT.find({'company': user_info['company']})))

        remained = 0
        if count % per_page > 0:
            remained = 1
        page_count = int(count / per_page) + remained

        if end_page > page_count:
            end_page = page_count

        pagination = {
            'start_page': start_page,
            'end_page': end_page,
            'page_block': page_block,
            'page_count': page_count
        }

        return render_template('profile.html', user_info=user_info, results=results, p=pagination)

    except jwt.ExpiredSignatureError:  # 해당 token의 로그인 시간이 만료시 login 페이지로 redirect
        return redirect(url_for("user.login"))
    except jwt.exceptions.DecodeError:  # 해당 token이 다르다면 login 페이지로 redirect
        return redirect(url_for("user.login"))
