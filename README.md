### SafetyManager
SafetyManager is a web solution for detecting whether or not wearing a helmet to prevent safety accidents at construction sites. This repository is where we keep a record of our SafetyManager-project progress

## Table of Contents
- [Project Introduction](#Project-Introduction)
- [Team](#Team)
- [Project-Rules](#Project-Rules)
- [Structure](#Structure)
- [Development](#Development)

<hr>

## Project-Introduction
- 주제 : 공사장 안전 사고 예방을 위한 안전모(헬멧) 착용 여부 탐지 Web 솔루션(SafetyManager) 개발
- 기간 : 2022.05.18 (수) ~ 2022.05.24 (화)

<hr>

## Team
- 김선민 [Git-hub](https://github.com/SeonminKim1)
- 김민기 [Git-hub](https://github.com/kmingky)
- 박재현 [Git-hub](https://github.com/Aeius)
- 황신혜 [Git-hub](https://github.com/hwanghye00)

<hr>

## Project-Rules
- Figma Mock-up : [Figma Link](https://www.figma.com/file/a1Exz8QZBzT5zlnk6SW1JQ/7%EC%A1%B0---Object-Detection-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8)
  - ![image](https://user-images.githubusercontent.com/33525798/170044696-64c1c1f6-525a-406b-8749-3318a71ed7e9.png)

- Schedule Management : [Git Project Link](https://github.com/SeonminKim1/SafetyManager/projects/1)
- Git Issue : [Git Issue Link](https://github.com/SeonminKim1/SafetyManager/issues)
- API Design : [Notion Link](https://www.notion.so/7383fb0f797b405396963e79db439f03?v=a9905b51cf8a458c99596d826cfe0acd)
- Tool
  - FE : HTML, CSS, JS
  - BE : Flask, Pytorch
  - DB : MongoDB (Atlas)
- DB Design
  - ![image](https://user-images.githubusercontent.com/33525798/170044904-4937d9f6-ec5f-4160-9d96-51fd800caf74.png)
  - User : 사용자 정보
    - 회사명(company) 속성을 통해 mypage에서 기업의 관리자가 사내 정보를 한 눈에 볼 수 있게 함 
  - Result : 서빙 모델 이용 기록
    - isPass, head, helmet, score 등의 Detecting 결과를 이용해 안전 여부를 판단 하고자 함
    - date : 작업 시간을 기록하여 월 별 통계 등을 집계 할 수 있게 함

<hr>

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

<hr>

## Development
#### Training
- 안전모 데이터와 Model을 Colab 로드 후 학습
- Dataset : Roboflow의 Hard Hat Worker Dataset (안전모 데이터셋) 사용
- Model : Open Source Object Detection Yolo v5 

#### Login / Register Page
- 회원가입, 로그인, 로그아웃 기능
- JWT 토큰 활용 쿠키 저장

#### Main Page
- 이미지/동영상 파일 업로드
- 이미지/동영상 Detect
- Detect 결과 출력 (Detect 이미지, 라벨값, Score 등)

#### Ranking Page
- 기업별 Score Ranking(현재 월) 구현
- View 페이지네이션 기능

#### MyPage
- 기업의 모든 User에 대한 결과 View
- View 페이지네이션 기능

#### etc
- 기능 및 소스코드 분리 작성 => 개발 생산성 최대화, 코드 충돌 최소화 지향
- BE에서 Detector 추론 모듈/ Web 모듈 분리
  - Detector 모듈 : Detection 결과 (Img, Video, 결과값을 이용한 Score 등) 리턴
  - Web Module : DB 연동, FE 요청에 따른 Detection 모듈 호출 및 응답
- Blueprints를 이용한 API Endpoint 분리
- Jinja의 include 문법을 이용한 nav.html 분리 및 Nav Bar 중복 구현 방지
