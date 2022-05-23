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
    # 현재 컴퓨터에 저장 된 'mytoken'인 쿠키 확인
    token_receive = request.cookies.get('mytoken')
    print('token_receive', token_receive)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.USER.find_one({"id": payload['id']})  # id, name, pwd, company
        return render_template('/index.html')
    except jwt.ExpiredSignatureError:  # 해당 token의 로그인 시간이 만료시 login 페이지로 redirect
        print('1')
        return redirect(url_for("user.login"))
    except jwt.exceptions.DecodeError:  # 해당 token이 다르다면 login 페이지로 redirect
        print('2')
        return redirect(url_for("user.login"))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
