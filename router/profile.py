from flask import Flask, jsonify, request, render_template, redirect, url_for
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
    # # 현재 컴퓨터에 저장 된 'mytoken'인 쿠키 확인
    # token_receive = request.cookies.get('mytoken')
    # print(token_receive)
    # 암호화되어있는 token의 값 디코딩(암호화 풀기)
    # payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    
    user_info = db.USER.find_one({"id": 'id'})
    results = list(db.result.find({
        'company':user_info['company'], 
    }))

    for i, res in enumerate(results):
        results[i]['predict_path'] = '../' + str(res['predict_path'])

    return render_template('profile.html', results = results)