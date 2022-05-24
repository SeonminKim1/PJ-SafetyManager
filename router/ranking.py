from flask import Flask, jsonify, request, render_template
import jwt
from flask import Blueprint
from werkzeug.utils import secure_filename
from datetime import datetime
import datetime
import certifi
from operator import itemgetter
import pymongo

SECRET_KEY = '$lucky7'
WEIGHTS_PATH = 'detector/weights/best.pt'

# DB 연결 코드
from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://luckyseven:luckyseven@cluster0.2hyld.mongodb.net/myFirstDatabase?retryWrites=true&w=majority',
    tlsCAFile=certifi.where())
db = client.od_project

from detector.detect import detect_run

bp = Blueprint("ranking", __name__, url_prefix="/ranking")

@bp.route('/', methods=['GET'])
def ranking():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.USER.find_one({'id': payload['id']})

    # 기업 리스트를 담을 변수 선언
    company_list = []
    # 모든 결과 불러오기
    result_list = list(db.RESULT.find({}, {'_id': False}))
    print(result_list)
    # 결과 리스트에서 기업만 중복제거하여 분류
    for result in result_list:
        if result['company'] not in company_list:
            company_list.append(result['company'])
    print(company_list)

    # 각 기업의 결과 중 최고점수만 분류
    company_high_score = []
    for company_name in company_list:
        company_info = list(db.RESULT.find({'company': company_name}, {'company': True,
                                                                       'score': True,
                                                                       'date': True,
                                                                       '_id': False}))
        print(company_info)

        # 오늘의 월만 추출하여 문자열화
        today_month = str(datetime.date.today().month)

        # 기업의 평균 score 저장
        avg_score = {'company': company_name, 'score': 0}
        score_total = 0.0

        for company in company_info:
            if company['score'] is not None: # score값이 Null인 경우 방지
                if company['date'][5:7] == today_month.zfill(2): # 저장되어있는 월과 오늘 월이 같을 경우만
                    score_total = company['score'] + score_total
                    avg_score['score'] = round(score_total / len(company_info), 3)

        company_high_score.append(avg_score)
        # 데이터 score를 기준으로 내림 차순
        sort_data = sorted(company_high_score, key=itemgetter('score'), reverse=True)
    print(sort_data)

    current_page = request.args.get("page", type=int, default=1)
    per_page = 10
    start_row = (current_page - 1) * per_page + 1
    end_row = start_row + per_page - 1
    rankings = sort_data[start_row:end_row]

    page_block = 1
    start_page = int((current_page - 1) / page_block * page_block + 1)
    end_page = start_page + page_block - 1
    count = len(sort_data)

    remained = 0
    if count % per_page > 0:
        remained = 1
    page_count = int(count / per_page) + remained

    if end_page > page_count:
        end_page = page_count

    return render_template('/ranking.html',
                           ranking=rankings,
                           current_page=current_page,
                           start_page=start_page,
                           end_page=end_page,
                           page_count=page_count,
                           page_block=page_block,
                           today_month=today_month,
                           user_info=user_info)
