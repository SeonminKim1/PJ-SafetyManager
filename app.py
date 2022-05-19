from flask import Flask, render_template, request, jsonify, redirect, url_for
import certifi

app = Flask(__name__)

SECRET_KEY = '$lucky7'

# DB 연결 코드
from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://luckyseven:luckyseven@cluster0.2hyld.mongodb.net/myFirstDatabase?retryWrites=true&w=majority',
    tlsCAFile=certifi.where())
db = client.luckyseven

from detector.detect import detect_run

@app.route('/main')
def main():
    result_path = detect_run()
    return render_template('index.html', result_path=result_path)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)