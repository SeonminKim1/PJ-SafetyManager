from flask import Flask, render_template, request, jsonify, redirect, url_for
import certifi

# Import detector/main.py, detect.py
from router import main, detect

app = Flask(__name__)

app.register_blueprint(main.bp) #/main
app.register_blueprint(detect.bp) #/detect

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
    return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
