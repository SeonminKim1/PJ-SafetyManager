from flask import Flask, render_template, request, jsonify, redirect, url_for
import jwt
import certifi

# Import detector/main.py, detect.py
from router import main, ranking, detect, user

app = Flask(__name__)

app.register_blueprint(main.bp)  # /main
app.register_blueprint(ranking.bp)  # /ranking
app.register_blueprint(detect.bp)  # /detect
app.register_blueprint(user.bp)  # /user

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
    token_receive = request.cookies.get('mytoken')
    print(token_receive)
    try:
        # 웹 접속자가 가지고 있는 token을 시크릿키로 디코딩
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        # payload 안에 id가 들어있습니다. 이 id로 유저정보 조회
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        # return jsonify({'result': 'success', 'nickname': userinfo['nick']})

    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})
    return render_template('/index.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
