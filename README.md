# SafeManager
Safe Manager Solution by Object Detection

### Run
```
python app.py
# static/test_data 밑 이미지 File 선택 후 업로드 및 추론
```

### Structure
```
├── detector // Yolov5 Detector Module
│   ├── models/
│   ├── utils/
│   ├── weights/  // 학습된 Weights 위치
│   ├── detect.py // detect 관련 소스코드
│   └── ...
│
├── static 
│   ├── css
│   ├── predict_data/ // Detect 결과 
│   ├── upload_data/  // 업로드 이미지
│   ├── test_data/    // 테스트용 이미지
│   └── ...
│
├── templates 
│   ├── index.html
│   └── ...
│
└── app.py // 메인
``` 