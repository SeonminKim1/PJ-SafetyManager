from flask import Flask, jsonify, request
from flask import Blueprint
import certifi

SECRET_KEY = '$lucky7'
WEIGHTS_PATH = 'detector/weights/best.pt'

# DB 연결 코드
from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://luckyseven:luckyseven@cluster0.2hyld.mongodb.net/myFirstDatabase?retryWrites=true&w=majority',
    tlsCAFile=certifi.where())
db = client.od_project

from detector.detect import detect_run

bp = Blueprint("detect", __name__, url_prefix="/detect")

@bp.route('/api/img/inference', methods=['POST'])
def img_detect_inference():
    upload_path = request.form['upload_path']
    filename, extension = upload_path.replace('static/upload_data', '').split('.')
 
    predict_path, results = detect_run(WEIGHTS_PATH, upload_path)
    predict_path = predict_path + '/' + filename + '.' + extension
    print('WEIGHTS_PATH: ', WEIGHTS_PATH)
    print('upload_path: ', upload_path)
    print('predict_path: ', predict_path)
    print('results', results)

    # Num 정보 Update
    num_length = list(db.RESULT.find({}))
    if len(num_length)==0:
        num = 1
    else:
        num = len(num_length)

    # DB에 정보 Update
    db.RESULT.update_one({'upload_path': upload_path}, 
                         {'$set': {
                            'num': num,
                            'helmet': int(results['helmet']),
                            'head': int(results['head']),
                            'score': float(results['score']),
                            'isPass': bool(results['isPass']),
                            'predict_path': predict_path
                            }}
                        )
    return jsonify({'result':'success', 
                    'predict_path':predict_path, 'results':results,
                    'msg': '추론이 완료 되었습니다.'})

@bp.route('/api/video/inference', methods=['POST'])
def video_detect_inference():
    upload_path = request.form['upload_path']
    filename, extension = upload_path.replace('static/upload_data', '').split('.')
    # upload_path = 'static/upload_data/' + filename + '.' + extension
 
    predict_path, results = detect_run(WEIGHTS_PATH, upload_path)
    predict_path = predict_path + filename + '.' + extension
    print('WEIGHTS_PATH: ', WEIGHTS_PATH)
    print('upload_path: ', upload_path)
    print('predict_path: ', predict_path)
    print('results', results)

    # Num 정보 Update
    num_length = list(db.RESULT.find({}))
    if len(num_length)==0:
        num = 1
    else:
        num = len(num_length)

    # DB에 정보 Update
    db.RESULT.update_one({'upload_path': upload_path}, 
                         {'$set': {
                            'num': num,
                            'helmet': int(results['helmet']),
                            'head': int(results['head']),
                            'score': float(results['score']),
                            'isPass': bool(results['isPass']),
                            'predict_path': predict_path
                            }}
                        )
    return jsonify({'result':'success', 
                    'predict_path':predict_path, 'results':results,
                    'msg': '추론이 완료 되었습니다.'})