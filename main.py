import os
import logging
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from models.schemas import (
    NutritionCalculationRequest,
    NutritionResponse,
    ErrorResponse,
    ComplexFood
)
from services.nutrition_service import NutritionCalculationService

# 환경변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(
    title="통합식품영양성분 계산 API",
    description="공공데이터포털의 통합식품영양성분정보를 활용한 영양성분 계산 서비스",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영환경에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 영양성분 계산 서비스 초기화
nutrition_service = NutritionCalculationService()


@app.get("/", tags=["기본"])
async def root():
    """API 기본 정보"""
    return {
        "service": "통합식품영양성분 계산 API",
        "version": "1.0.0",
        "description": "공공데이터포털 API를 활용한 음식별 영양성분 계산 서비스",
        "endpoints": {
            "docs": "/docs",
            "foods": "/foods",
            "calculate": "/calculate-nutrition",
            "health": "/health"
        }
    }


@app.get("/health", tags=["기본"])
async def health_check():
    """헬스체크 엔드포인트"""
    return {
        "status": "healthy",
        "service": "nutrition-calculator",
        "mock_mode": nutrition_service.api_client.use_mock
    }


@app.get("/foods", response_model=List[str], tags=["음식 정보"])
async def get_available_foods():
    """등록된 복합식품 목록 조회"""
    try:
        foods = nutrition_service.get_available_foods()
        return foods
    except Exception as e:
        logger.error(f"음식 목록 조회 실패: {e}")
        raise HTTPException(status_code=500, detail="음식 목록 조회에 실패했습니다.")


@app.get("/foods/{food_name}", response_model=ComplexFood, tags=["음식 정보"])
async def get_food_composition(food_name: str):
    """특정 음식의 구성요소 정보 조회"""
    try:
        composition = nutrition_service.get_food_composition(food_name)
        if not composition:
            raise HTTPException(
                status_code=404, 
                detail=f"'{food_name}' 음식 정보를 찾을 수 없습니다."
            )
        return composition
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"음식 구성요소 조회 실패: {e}")
        raise HTTPException(status_code=500, detail="음식 구성요소 조회에 실패했습니다.")


@app.post("/calculate-nutrition", response_model=NutritionResponse, tags=["영양성분 계산"])
async def calculate_nutrition(request: NutritionCalculationRequest):
    """영양성분 계산"""
    try:
        logger.info(f"영양성분 계산 요청: {request.food_name} ({request.weight_grams}g)")
        
        # 요청 검증
        if request.weight_grams <= 0:
            raise HTTPException(
                status_code=400,
                detail="중량은 0보다 큰 값이어야 합니다."
            )
        
        # 영양성분 계산
        result = nutrition_service.calculate_nutrition(request)
        
        if not result:
            return NutritionResponse(
                success=False,
                message=f"'{request.food_name}' 영양성분 계산에 실패했습니다. 등록되지 않은 음식이거나 데이터 조회에 문제가 있습니다.",
                data=None
            )
        
        logger.info(f"영양성분 계산 완료: {request.food_name} - {result.energy}kcal")
        
        return NutritionResponse(
            success=True,
            message="영양성분 계산이 성공적으로 완료되었습니다.",
            data=result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"영양성분 계산 실패: {e}")
        raise HTTPException(
            status_code=500,
            detail="영양성분 계산 중 오류가 발생했습니다."
        )


@app.get("/calculate-nutrition/{food_name}/{weight_grams}", response_model=NutritionResponse, tags=["영양성분 계산"])
async def calculate_nutrition_get(food_name: str, weight_grams: float):
    """GET 방식 영양성분 계산 (간편 사용)"""
    request = NutritionCalculationRequest(
        food_name=food_name,
        weight_grams=weight_grams
    )
    return await calculate_nutrition(request)


@app.get("/ingredients/{ingredient_name}", tags=["재료 정보"])
async def get_ingredient_nutrition(ingredient_name: str):
    """개별 재료의 영양성분 정보 조회"""
    try:
        nutrition = nutrition_service.get_ingredient_nutrition(ingredient_name)
        
        if not nutrition:
            raise HTTPException(
                status_code=404,
                detail=f"'{ingredient_name}' 재료의 영양성분 정보를 찾을 수 없습니다."
            )
        
        return {
            "success": True,
            "message": f"'{ingredient_name}' 영양성분 정보 조회 완료",
            "data": nutrition.model_dump()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"재료 영양성분 조회 실패: {e}")
        raise HTTPException(
            status_code=500,
            detail="재료 영양성분 조회에 실패했습니다."
        )


# 예외 처리 핸들러
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """일반 예외 처리"""
    logger.error(f"예상치 못한 오류: {exc}")
    return ErrorResponse(
        success=False,
        error_code="INTERNAL_ERROR",
        message="서버 내부 오류가 발생했습니다.",
        details=str(exc) if os.getenv('DEBUG', 'false').lower() == 'true' else None
    )


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', '8000'))
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    
    logger.info(f"서버 시작: http://{host}:{port}")
    logger.info(f"API 문서: http://{host}:{port}/docs")
    logger.info(f"Mock 모드: {nutrition_service.api_client.use_mock}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        log_level=os.getenv('LOG_LEVEL', 'info').lower()
    )