from flask import Flask, jsonify, request, render_template
from flask import Blueprint
from werkzeug.utils import secure_filename
from datetime import datetime
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
    # 기업 리스트를 담을 변수 선언
    company_list = []
    # 모든 결과 불러오기
    result_list = list(db.result.find({}, {'_id': False}))
    print(result_list)
    # 결과 리스트에서 기업만 중복제거하여 분류
    for result in result_list:
        if result['company'] not in company_list:
            company_list.append(result['company'])
    print(company_list)

    # 각 기업의 결과 중 최고점수만 분류
    company_high_score = []
    for company_name in company_list:
        company_info = list(db.result.find({'company': company_name}, {'company': True, 'score': True, '_id': False}))
        print(company_info)
        avg_score = {'company': company_name, 'score': 0}
        score_total = 0.0

        for company in company_info:
            if company['score'] is not None:
                score_total = company['score'] + score_total
                avg_score['score'] = round(score_total / len(company_info), 3)

        company_high_score.append(avg_score)
        sort_data = sorted(company_high_score, key=itemgetter('score'), reverse=True)
    print(sort_data)

    return render_template('/ranking.html', ranking=sort_data)
