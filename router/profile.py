from flask import Flask, jsonify, request, render_template
from flask import Blueprint
from werkzeug.utils import secure_filename
from datetime import datetime
import certifi

SECRET_KEY = '$lucky7'
WEIGHTS_PATH = 'detector/weights/best.pt'

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
    token_receive = request.cookies.get('mytoken')
    try:
        # 암호화되어있는 token의 값 디코딩(암호화 풀기)
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        feed_nickname = request.args.get('feed_nickname')

        user_info = db.USER.find_one({"nickname": feed_nickname})  # id, num, nickname, feed_images, content, like, reply
        my_feed_list = list(db.FEED.find({"nickname": feed_nickname}))
        # print(my_feed_list)

        post_count = len(my_feed_list)
        follower_count = len(user_info['follower'])
        following_count = len(user_info['following'])

        my_follower_list = []
        for my_followers in user_info['follower']:
            my_follower = db.USER.find_one({'nickname': my_followers})
            my_follower_list.append(my_follower)

        my_following_list = []
        for my_followings in user_info['following']:
            my_following = db.USER.find_one({'nickname': my_followings})
            my_following_list.append(my_following)

        return render_template('profile.html')

    except jwt.ExpiredSignatureError:  # 해당 token의 로그인 시간이 만료시 login 페이지로 redirect
        return redirect(url_for("login"))
    except jwt.exceptions.DecodeError:  # 해당 token이 다르다면 login 페이지로 redirect
        return redirect(url_for("login"))