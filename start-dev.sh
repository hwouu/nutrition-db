#!/bin/bash

# 개발 환경 시작 스크립트

echo "🚀 영양성분 계산기 개발 환경을 시작합니다..."

# 백엔드 서버 시작 (백그라운드)
echo "📡 백엔드 서버 시작 중..."
cd "$(dirname "$0")"
source venv/bin/activate
python main.py &
BACKEND_PID=$!

# 잠시 대기 (백엔드 서버 준비 시간)
sleep 3

# 프론트엔드 서버 시작 (백그라운드)
echo "🎨 프론트엔드 서버 시작 중..."
cd frontend
npm run dev &
FRONTEND_PID=$!

# 서버 정보 출력
echo ""
echo "✅ 개발 환경이 성공적으로 시작되었습니다!"
echo ""
echo "🔗 서비스 주소:"
echo "   • 프론트엔드: http://localhost:5173"
echo "   • 백엔드 API: http://localhost:8000"
echo "   • API 문서: http://localhost:8000/docs"
echo ""
echo "⏹️  종료하려면 Ctrl+C를 누르세요"

# 종료 핸들러
cleanup() {
    echo ""
    echo "🛑 서버를 종료합니다..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT

# 백그라운드 프로세스 대기
wait