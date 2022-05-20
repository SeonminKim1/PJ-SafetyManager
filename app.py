from flask import Flask, render_template, request, jsonify, redirect, url_for
import certifi
from werkzeug.utils import secure_filename
from datetime import datetime
from router import main

app = Flask(__name__)

app.register_blueprint(main.bp) #/main

SECRET_KEY = '$lucky7'
WEIGHTS_PATH = 'detector/weights/best.pt'

# DB 연결 코드
from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://luckyseven:luckyseven@cluster0.2hyld.mongodb.net/myFirstDatabase?retryWrites=true&w=majority',
    tlsCAFile=certifi.where())
db = client.od_project

from detector.detect import detect_run


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/main/api/img/upload', methods=['POST'])
def file_upload():
    # 업로드 파일 받아오기.
    file = request.files['file']  # werkzeug.datastructures.FileStorage, name
    extension = secure_filename(file.filename).split('.')[-1]  # file.filename /
    f_name = file.filename.replace('.' + extension, '')  # test1, 확장자 제거

    # 파일 이름 , Local에 Upload 한 이미지 저장 
    today = datetime.now()
    today = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f_name + '-' + today  # test1-2022-05-19-14-43-23.jpg
    upload_path = 'static/upload_data/' + filename + '.' + extension
    file.save(upload_path)  # 'static/upload_data/test1.jpg

    predict_path = detect_run(WEIGHTS_PATH, upload_path) + '/' + filename + '.' + extension
    print('WEIGHTS_PATH: ', WEIGHTS_PATH)
    print('upload_path: ', upload_path)
    print('predict_path: ', predict_path)

    # DB에 Image Path 저장
    doc = {
        'id': 'id',
        'company': 'samsung',
        'isPass': True,
        'helmet': 0,
        'head': 0,
        'score': 0.0,
        'date': today,
        'upload_path': upload_path,
        'predict_path': predict_path
    }
    db.result.insert_one(doc)
    return jsonify({'result': 'success', 'predict_path': predict_path})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
