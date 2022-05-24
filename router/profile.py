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

        # page 파라미터 가져오기 없을경우 기본값 1 지정
        page = request.args.get('page', type=int, default=1)
        per_page = 8  # 한 페이지에 출력할 게시물 수

        results = sorted(
            list(db.RESULT.find({'company': user_info['company']})), key=lambda x: x['date'], reverse=True)

        # 페이지에 맞는 첫 게시물 번호, 마지막 게시물 번호
        start_row = (page - 1) * per_page + 1
        end_row = start_row + per_page - 1

        # 정리 끝난 list의 페이지에 맞게 출력하기 ex) page=1 일경우 0~9까지 page=2일경우 10~19 되도록
        results = results[start_row - 1:end_row]

        for i, res in enumerate(results):
            results[i]['upload_path'] = '../' + str(res['upload_path'])
            results[i]['predict_path'] = '../' + str(res['predict_path'])

        # 페이징 숫자 ex) 이전 1 2 3 4 5 다음 >> 이 경우는 5
        page_block = 1

        # 보여줄 페이징 번호들중 가장 첫번째, 마지막 번호 지정 ex) page=2 여도 1 2 3 4 5 가 출력되도록
        start_page = int((page - 1) / page_block * page_block + 1)
        end_page = start_page + page_block - 1

        count = len(list(db.RESULT.find({'company': user_info['company']})))
        # 마지막 번호의 경우 게시물에 맞춰줘야한다 ex) 블록이 5여도 게시물이 모자라면 이전 1 2 3 다음 처럼 출력되도록
        remained = 0
        if count % per_page > 0:
            remained = 1
        page_count = int(count / per_page) + remained  # 파이썬에서 자동형변환 안되어서 명시적 형변환 필수
        if end_page > page_count:
            end_page = page_count

        # 출력 시 필요한 데이터들 모아서 리턴
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
