from flask import Flask, render_template, request, jsonify, redirect, url_for
import jwt
import hashlib
import certifi
from werkzeug.utils import secure_filename
from datetime import datetime
from router import main, ranking

# Import detector/main.py, detect.py
from router import main, detect

app = Flask(__name__)

app.register_blueprint(main.bp) #/main
app.register_blueprint(ranking.bp) #/ranking
app.register_blueprint(detect.bp) #/detect

SECRET_KEY = '$lucky7'
WEIGHTS_PATH = 'detector/weights/best.pt'

# DB 연결 코드
from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://luckyseven:luckyseven@cluster0.2hyld.mongodb.net/myFirstDatabase?retryWrites=true&w=majority',
    tlsCAFile=certifi.where())
db = client.od_project

@app.route('/')
def home():
    return render_template('/login.html')


# ================ Join Page ================ #
@app.route('/join')
def join():
    return render_template('/join.html')


# 회원가입 입력값을 받아 DB에 추가하기
@app.route("/api/join", methods=["POST"])
def api_join():
    id_receive = request.form['id_give']
    company_receive = request.form['company_give']
    pwd_receive = request.form['pwd_give']

    # 입력받은 패스워드 값 해싱하여 암호화
    hashed_pw = hashlib.sha256(pwd_receive.encode('utf-8')).hexdigest()

    doc = {
        'id': id_receive,
        'company': company_receive,
        'pwd': hashed_pw,
    }
    db.USER.insert_one(doc)

    return jsonify({'msg': '회원 가입 완료'})


# ================ Login / Logout Page ================ #
@app.route('/login')
def login():
    return render_template('/login.html')


# 로그인 id, company, pwd 값 판별 후 토큰 생성
@app.route("/api/login", methods=["POST"])
def api_login():
    id_receive = request.form['id_give']
    company_receive = request.form['company_give']
    pwd_receive = request.form['pwd_give']

    # 입력받은 패스워드 값 해싱하여 암호화
    hashed_pw = hashlib.sha256(pwd_receive.encode('utf-8')).hexdigest()

    # DB에 저장된 값 가져오기
    user = db.USER.find_one({'id': id_receive, 'company': company_receive, 'pwd': hashed_pw})
    print(user)

    if user is not None:
        # JWT(Json Wep Token)생성
        # 토큰을 풀었을 때 얻을 수 있는 id 값과, 유효기간(exp)를 담음
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=1800)
        }
        # 토큰 생성 payload의 값 인코딩, 암호키 필수 유출금지!, 암호화형태 지정
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token, 'msg': '로그인 성공'})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디 또는 비밀번호가 일치하지 않습니다.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
