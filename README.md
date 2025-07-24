# 🥗 영양성분 계산기 (Nutrition Calculator)

한국 공공데이터포털의 **전국통합식품영양성분정보(원재료성식품)표준데이터**를 활용한 웹 기반 영양성분 계산 서비스입니다.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)
![React](https://img.shields.io/badge/React-18.3.1-blue.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5.5.3-blue.svg)
![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-3.4.1-blue.svg)

## 🎯 주요 기능

### 💡 핵심 비즈니스 로직
- **음식명 + 중량 입력**: 사용자가 원하는 음식과 정확한 중량 입력
- **복합 음식 분석**: 감자샐러드 = 감자(60%) + 마요네즈(25%) + 계란(15%)
- **상세 영양성분**: 20여 가지 영양소 (칼로리, 3대 영양소, 비타민, 미네랄)
- **계산 기록 저장**: 로컬스토리지 활용한 이전 계산 결과 캐싱
- **데이터 출처 명시**: 공공데이터포털 정보 및 현재 Mock 데이터 사용 안내

### 🔧 백엔드 (FastAPI)
- 공공데이터 API 연동 준비 (현재 Mock 데이터)
- 복합식품 원재료 분해 계산
- RESTful API 설계
- 자동 API 문서 생성 (Swagger/ReDoc)
- CORS 미들웨어 설정

### 🎨 프론트엔드 (React + TypeScript)
- **사용자 친화적 UI**: 음식명/중량 입력 폼
- **영양성분 카드**: 칼로리, 단백질, 탄수화물, 지방 대형 표시
- **상세 정보**: 미네랄, 비타민 상세 표시
- **원재료 구성**: 재료별 비율 및 실제 중량 계산
- **계산 기록**: 타임스탬프와 함께 이전 결과 저장/표시
- **반응형 디자인**: 모바일/데스크톱 최적화

## 🏗️ 기술 스택

### Backend
- **Python 3.12** - 메인 언어
- **FastAPI** - 웹 프레임워크
- **Pydantic** - 데이터 검증
- **Requests** - HTTP 클라이언트
- **Uvicorn** - ASGI 서버

### Frontend
- **React 18** - UI 라이브러리
- **TypeScript** - 타입 안전성
- **Vite** - 빌드 도구
- **Tailwind CSS** - 스타일링
- **React Query** - 상태 관리
- **Lucide React** - 아이콘

## 🚀 빠른 시작

### 1. 저장소 클론
```bash
git clone https://github.com/hwouu/nutrition-db.git
cd nutrition-db
```

### 2. 백엔드 설정
```bash
# Python 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는 venv\Scripts\activate  # Windows

# 의존성 설치
pip install -r requirements.txt
```

### 3. 프론트엔드 설정
```bash
cd frontend
npm install
```

### 4. 환경변수 설정
```bash
# 백엔드 환경변수 (.env 파일이 이미 설정됨)
# 실제 공공데이터 API 키가 있다면 .env 파일에서 SERVICE_KEY 수정
# 현재는 Mock 데이터 모드로 설정됨 (USE_MOCK_DATA=true)
```

### 5. 개발 서버 실행

#### 방법 1: 스크립트 사용 (권장)
```bash
./start-dev.sh
```

#### 방법 2: 개별 실행
```bash
# 터미널 1: 백엔드 서버
source venv/bin/activate
python main.py

# 터미널 2: 프론트엔드 서버  
cd frontend
npm run dev
```

## 🌐 서비스 접속

- **프론트엔드**: http://localhost:5173
- **백엔드 API**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📊 등록된 음식

현재 시스템에 등록된 복합식품:
1. **감자샐러드** - 감자(60%) + 마요네즈(25%) + 계란(15%)
2. **야채샐러드** - 양파(40%) + 당근(35%) + 마요네즈(25%)
3. **계란프라이** - 계란(90%)
4. **감자튀김** - 감자(100%)
5. **감자전** - 감자(80%) + 계란(15%)
6. **양파볶음** - 양파(100%)
7. **당근볶음** - 당근(100%)
8. **스크램블에그** - 계란(100%)
9. **오믈렛** - 계란(70%) + 양파(20%) + 당근(10%)
10. **샐러드** - 양파(30%) + 당근(30%) + 감자(25%) + 마요네즈(15%)

## 🔧 API 사용 예시

### 영양성분 계산
```bash
# POST 방식
curl -X POST http://localhost:8000/calculate-nutrition \
     -H "Content-Type: application/json" \
     -d '{"food_name": "감자샐러드", "weight_grams": 150}'

# GET 방식 (간편)
curl http://localhost:8000/calculate-nutrition/감자샐러드/150
```

### 응답 예시
```json
{
  "success": true,
  "message": "영양성분 계산이 성공적으로 완료되었습니다.",
  "data": {
    "food_name": "감자샐러드",
    "weight_grams": 150.0,
    "energy": 356.48,
    "protein": 5.12,
    "fat": 30.44,
    "carbohydrate": 18.67,
    "sugar": 1.88,
    "dietary_fiber": 3.0,
    "calcium": 43.2,
    "iron": 1.17,
    "sodium": 327.6,
    "potassium": 454.5
  }
}
```

## 🧪 테스트

### 백엔드 테스트
```bash
# API 연결 테스트
python test_api.py

# 통합 테스트
python test_integration.py
```

### 프론트엔드 테스트
```bash
cd frontend
npm test
```

## 📁 프로젝트 구조

```
nutrition-db/
├── 📦 백엔드 (Python/FastAPI)
│   ├── api/                 # API 클라이언트
│   ├── models/              # 데이터 모델
│   ├── services/            # 비즈니스 로직
│   ├── data/               # 음식 구성요소 데이터
│   ├── tests/              # 테스트 파일
│   ├── main.py             # FastAPI 서버
│   └── requirements.txt    # Python 의존성
│
├── 🎨 프론트엔드 (React/TypeScript)  
│   ├── src/
│   │   ├── components/     # React 컴포넌트
│   │   │   ├── Layout/     # 레이아웃 컴포넌트
│   │   │   ├── Dashboard/  # 대시보드 컴포넌트
│   │   │   └── UI/         # 재사용 UI 컴포넌트
│   │   ├── services/       # API 클라이언트
│   │   ├── types/          # TypeScript 타입
│   │   ├── hooks/          # Custom React Hooks
│   │   └── utils/          # 유틸리티 함수
│   ├── package.json        # Node.js 의존성
│   └── vite.config.ts      # Vite 설정
│
└── 📜 설정 파일
    ├── .env                # 환경변수
    ├── start-dev.sh        # 개발 서버 시작 스크립트
    └── README.md           # 프로젝트 문서
```

## 🔧 설정 옵션

### 환경변수 (.env)
```bash
# 공공데이터 API 키
SERVICE_KEY=your_api_key_here

# API 설정
API_BASE_URL=http://api.data.go.kr/openapi/tn_pubr_public_nutri_material_info_api
USE_MOCK_DATA=true        # Mock 데이터 사용 여부

# 서버 설정
HOST=0.0.0.0
PORT=8000
DEBUG=true
```

## 🚀 배포

### Docker 사용
```bash
# TODO: Docker 설정 추가 예정
```

### 수동 배포
```bash
# 프론트엔드 빌드
cd frontend
npm run build

# 백엔드는 main.py 실행
python main.py
```

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다.

## 📝 TODO

### 🔥 높은 우선순위
- [ ] **공공데이터 API 연동**: 인증키 설정 및 실제 API 연결
- [ ] **음식 데이터베이스 확장**: 더 많은 복합 음식 레시피 추가
- [ ] **사용자 입력 개선**: 자동완성 및 검색 기능 구현
- [ ] **영양 목표 설정**: 일일 권장량 대비 비교 기능

### 🚀 중간 우선순위
- [ ] **데이터 시각화**: 영양성분 차트 및 그래프 추가
- [ ] **즐겨찾기 기능**: 자주 조회하는 음식 즐겨찾기
- [ ] **영양 분석**: 영양 균형 분석 및 권장사항 제공
- [ ] **단위 변환**: oz, lb 등 다양한 단위 지원
- [ ] **음식 조합**: 여러 음식 조합 시 총 영양성분 계산

### 💡 낮은 우선순위
- [ ] **사용자 계정**: 회원가입 및 로그인 시스템
- [ ] **식단 관리**: 일일/주간 식단 계획 및 관리
- [ ] **모바일 앱**: React Native를 이용한 모바일 버전
- [ ] **다국어 지원**: 영어, 중국어 등 다국어 인터페이스
- [ ] **소셜 공유**: 영양성분 결과 SNS 공유 기능

### 🛠 기술 개선
- [ ] **성능 최적화**: React Query 캐싱 전략 개선
- [ ] **에러 처리**: 더 상세한 에러 메시지 및 복구 방안
- [ ] **테스트 코드**: 백엔드/프론트엔드 단위 테스트 추가
- [ ] **Docker 지원**: 컨테이너 기반 배포 환경 구축
- [ ] **CI/CD**: GitHub Actions를 이용한 자동 배포

### 🔧 버그 수정
- [ ] **중량 입력 검증**: 음수값 및 비정상 입력 처리 개선
- [ ] **네트워크 오류**: API 호출 실패 시 재시도 로직 추가
- [ ] **브라우저 호환성**: Safari 등 구형 브라우저 지원

## 📊 데이터 출처

본 프로젝트는 [공공데이터포털](https://www.data.go.kr/)에서 제공하는 다음 데이터를 활용합니다:

- **데이터명**: 전국통합식품영양성분정보(원재료성식품)표준데이터
- **제공기관**: 농촌진흥청
- **데이터 링크**: https://www.data.go.kr/data/15100065/standard.do

> ⚠️ **현재 상태**: API 인증키 동기화 문제로 Mock 데이터를 사용하여 서비스를 제공하고 있습니다.

## 💡 사용법

### 1. 기본 사용 흐름
1. 웹사이트 접속 후 **음식명** 입력 (예: "감자샐러드")
2. **중량(g)** 입력 (예: 300g)
3. **"계산하기"** 버튼 클릭
4. 영양성분 결과 확인

### 2. 사용 가능한 음식
화면에 표시되는 음식 태그를 클릭하면 자동으로 입력됩니다:
- 감자샐러드, 야채샐러드, 계란프라이, 감자튀김, 감자전
- 양파볶음, 당근볶음, 스크램블에그, 오믈렛, 샐러드

### 3. 결과 해석
- **기본 영양성분**: 칼로리, 단백질, 탄수화물, 지방 (대형 컬러 카드)
- **상세 영양성분**: 미네랄(칼슘, 철분, 나트륨, 칼륨), 비타민(A, C), 기타(당류, 식이섬유)
- **원재료 구성**: 복합 음식의 재료별 비율과 실제 중량
- **재료별 영양성분**: 각 재료의 개별 영양성분 분해 (상세보기 토글)

### 4. 계산 기록 활용
- 계산 결과는 자동으로 로컬스토리지에 저장됩니다 (최대 10개)
- "계산 기록" 섹션에서 이전 결과를 확인할 수 있습니다
- 타임스탬프와 함께 음식명, 중량, 주요 영양소가 요약 표시됩니다

## 🎯 프로젝트 목표

이 프로젝트는 단순한 칼로리 계산기를 넘어서, **과학적이고 정확한 영양성분 분석**을 목표로 합니다:

1. **정확성**: 공공데이터 기반의 신뢰할 수 있는 영양정보
2. **실용성**: 실제 사용 가능한 음식 중량을 고려한 계산
3. **교육성**: 음식의 구성과 영양소 분포에 대한 이해 증진
4. **접근성**: 누구나 쉽게 사용할 수 있는 직관적인 인터페이스

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 GitHub Issues를 통해 제출해 주세요.

---

<div align="center">

**🥗 건강한 식단 관리의 시작, 영양성분 계산기**

Made with ❤️ and ☕ for better nutrition awareness

</div>
