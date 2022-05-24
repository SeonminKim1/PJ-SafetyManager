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
            if company['score'] is not None:  # score값이 Null인 경우 방지
                if company['date'][5:7] == today_month.zfill(2):  # 저장되어있는 월과 오늘 월이 같을 경우만
                    score_total = company['score'] + score_total
                    avg_score['score'] = round(score_total / len(company_info), 3)

        company_high_score.append(avg_score)
        # 데이터 score를 기준으로 내림 차순
        sort_data = sorted(company_high_score, key=itemgetter('score'), reverse=True)
    print(sort_data)

    # page 값 가져오기 없을 경우 기본값 1
    current_page = request.args.get("page", type=int, default=1)
    # 한 페이지에 출력할 게시물 수
    per_page = 10
    # 페이지에 맞는 첫 게시물 번호, 마지막 게시물 번호
    start_row = (current_page - 1) * per_page + 1
    end_row = start_row + per_page - 1

    # 정리 끝난 list의 페이지에 맞게 출력하기 ex) page=1 일경우 0~9까지 page=2일경우 10~19 되도록
    rankings = sort_data[start_row - 1:end_row]

    # 페이지 블록 = 이전 1 2 3 4 5 다음 >> 이경우 블록 = 5
    page_block = 1

    # 보여줄 페이징 번호들중 가장 첫번째, 마지막 번호 지정 ex) page=2 여도 1 2 3 4 5 가 출력되도록
    start_page = int((current_page - 1) / page_block * page_block + 1)
    end_page = start_page + page_block - 1

    # 마지막 번호의 경우 게시물에 맞춰줘야한다 ex) 블록이 5여도 게시물이 모자라면 이전 1 2 3 다음 처럼 출력되도록
    count = len(sort_data)
    remained = 0
    if count % per_page > 0:
        remained = 1
    page_count = int(count / per_page) + remained  # 파이썬에서 자동형변환 안되어서 명시적 형변환 필수
    if end_page > page_count:
        end_page = page_count

    # 출력 시 필요한 데이터들 모아서 리턴
    pagination = {
        'current_page': current_page,
        'start_page': start_page,
        'end_page': end_page,
        'page_count': page_count,
        'page_block': page_block,
    }

    return render_template('/ranking.html',
                           ranking=rankings,
                           p=pagination,
                           today_month=today_month,
                           user_info=user_info)
