# SafeManager
Safe Manager Solution by Object Detection

### Run
```
python app.py
# static/test_data 밑 이미지 File 선택 후 업로드 및 추론
```

### Structure
```
├── detector          // Yolov5 Detector Module
│   ├── models/       // BackBone
│   ├── utils/        // box 라벨값 Draw
│   ├── detect.py     // detect 관련 소스코드
│   └── ...
│
├── routers           // API Endpoint (Blueprints)
│   ├── main.py       // Upload 및 기본 기능 API
│   ├── detect.py     // Detection 요청 API
│   ├── profile.py    // Mypage 정보 조회 API
│   ├── ranking.py    // Ranking 정보 조회 API
│   └── user.py       // user 회원가입/로그인 API
│
├── static 
│   ├── css/          // css
│   ├── js/           // JS
│   ├── predict_data/ // Detect 결과 
│   ├── upload_data/  // 업로드 이미지
│   └── test_data/    // 테스트용 이미지
│
├── templates 
│   ├── nav.html      // nav Page
│   ├── index.html    // Main Page
│   ├── profile.html  // MyPage 
│   ├── ranking.html  // Ranking Page
│   ├── login.html    // Login Page
│   └── join.html     // Join Page
│
├── training 
│   └── training code // colab용 학습코드 
│
└── app.py // 메인
```