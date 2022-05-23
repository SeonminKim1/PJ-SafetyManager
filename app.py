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
    return render_template('/index.html')

    # 컴퓨터에 저장된 'mytoken' 쿠키 확인
    token_receive = request.cookies.get('mytoken')
    try:
        # 암호화 된 token 값 디코딩
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

    except jwt.ExpiredSignatureError:  # 해당 token 로그인 시간이 만료시 login 페이지로 이동
        return redirect(url_for("login"))
    except jwt.exceptions.DecodeError:  # 해당 token이 다르다면 login 페이지로 이동
        return redirect(url_for("login"))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
