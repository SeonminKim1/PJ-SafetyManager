from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
from flask import Blueprint
import jwt
import hashlib
import certifi
import datetime

app = Flask(__name__)

SECRET_KEY = '$lucky7'
WEIGHTS_PATH = 'detector/weights/best.pt'

# DB 연결 코드
from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://luckyseven:luckyseven@cluster0.2hyld.mongodb.net/myFirstDatabase?retryWrites=true&w=majority',
    tlsCAFile=certifi.where())
db = client.od_project

bp = Blueprint("user", __name__, url_prefix="/user")


# ================ Join Page ================ #
@bp.route('/join')
def join():
    return render_template('/join.html')


# 회원가입 입력값을 받아 DB에 추가하기
@bp.route("/api/join", methods=["POST"])
def api_join():
    id_receive = request.form['id_give']
    name_receive = request.form['name_give']
    company_receive = request.form['company_give']
    pwd_receive = request.form['pwd_give']

    # 입력받은 패스워드 값 해싱하여 암호화
    hashed_pw = hashlib.sha256(pwd_receive.encode('utf-8')).hexdigest()

    doc = {
        'id': id_receive,
        'name': name_receive,
        'company': company_receive,
        'pwd': hashed_pw,
    }
    db.USER.insert_one(doc)

    return jsonify({'msg': '회원 가입 완료'})


# ================ Login / Logout Page ================ #
@bp.route('/login')
def login():
    return render_template('/login.html')


# 로그인 id, company, pwd 값 판별 후 토큰 생성
@bp.route("/api/login", methods=["POST"])
def api_login():
    id_receive = request.form['id_give']
    pwd_receive = request.form['pwd_give']

    # 입력받은 패스워드 값 해싱하여 암호화
    hashed_pw = hashlib.sha256(pwd_receive.encode('utf-8')).hexdigest()

    # DB에 저장된 값 가져오기
    user = db.USER.find_one({'id': id_receive, 'pwd': hashed_pw})
    print(user)

    if user is not None:
        # JWT(Json Wep Token)생성
        # 토큰을 풀었을 때 얻을 수 있는 id 값과, 유효기간(exp)를 담음
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=1800)
        }
        print(payload)
        # 토큰 생성 payload의 값 인코딩, 암호키 필수 유출금지!, 암호화형태 지정
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        print(token)

        return jsonify({'result': 'success', 'token': token, 'msg': '로그인 성공'})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디 또는 비밀번호가 일치하지 않습니다.'})

@bp.route('/logout')
def logout():
    token_receive = request.cookies.get('mytoken')
    if token_receive is not None:
        return jsonify({'msg': '로그아웃 완료'})
