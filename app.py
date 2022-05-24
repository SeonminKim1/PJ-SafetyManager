from flask import Flask, render_template, request, jsonify, redirect, url_for
import jwt
import certifi

# Import detector/main.py, detect.py
from router import main, ranking, detect, profile, user

app = Flask(__name__)

app.register_blueprint(main.bp) #/main
app.register_blueprint(ranking.bp) #/ranking
app.register_blueprint(profile.bp) #/profile
app.register_blueprint(detect.bp) #/detect
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

    try:
        # 웹 접속자가 가지고 있는 token을 시크릿키로 디코딩
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # payload 안에 id가 들어있습니다. 이 id로 유저정보 조회
        user_info = db.USER.find_one({'id': payload['id']}, {'_id': 0})
        # return jsonify({'result': 'success', 'nickname': userinfo['nick']})

        return render_template('/index.html', user_info=user_info)

    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return render_template('/login.html')
    except jwt.exceptions.DecodeError:
        return render_template('/login.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
