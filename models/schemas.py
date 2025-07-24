from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from decimal import Decimal


class NutritionInfo(BaseModel):
    """영양성분 정보 모델"""
    
    # 기본 정보
    food_code: str = Field(alias='foodCd', description="식품코드")
    food_name: str = Field(alias='foodNm', description="식품명")
    
    # 영양성분 기준량
    nutrition_base_amount: Optional[str] = Field(alias='nutConSrtrQua', default=None, description="영양성분함량기준량")
    
    # 주요 영양성분 (g 단위)
    energy: Optional[float] = Field(alias='enerc', default=None, description="에너지(kcal)")
    water: Optional[float] = Field(alias='water', default=None, description="수분(g)")
    protein: Optional[float] = Field(alias='prot', default=None, description="단백질(g)")
    fat: Optional[float] = Field(alias='fatce', default=None, description="지방(g)")
    ash: Optional[float] = Field(alias='ash', default=None, description="회분(g)")
    carbohydrate: Optional[float] = Field(alias='chocdf', default=None, description="탄수화물(g)")
    sugar: Optional[float] = Field(alias='sugar', default=None, description="당류(g)")
    dietary_fiber: Optional[float] = Field(alias='fibtg', default=None, description="식이섬유(g)")
    
    # 무기질 (mg 단위)
    calcium: Optional[float] = Field(alias='ca', default=None, description="칼슘(mg)")
    iron: Optional[float] = Field(alias='fe', default=None, description="철(mg)")
    phosphorus: Optional[float] = Field(alias='p', default=None, description="인(mg)")
    potassium: Optional[float] = Field(alias='k', default=None, description="칼륨(mg)")
    sodium: Optional[float] = Field(alias='nat', default=None, description="나트륨(mg)")
    
    # 비타민
    vitamin_a: Optional[float] = Field(alias='vitaRae', default=None, description="비타민 A(μg RAE)")
    retinol: Optional[float] = Field(alias='retol', default=None, description="레티놀(μg)")
    beta_carotene: Optional[float] = Field(alias='cartb', default=None, description="베타카로틴(μg)")
    thiamine: Optional[float] = Field(alias='thia', default=None, description="티아민(mg)")
    riboflavin: Optional[float] = Field(alias='ribf', default=None, description="리보플라빈(mg)")
    niacin: Optional[float] = Field(alias='nia', default=None, description="니아신(mg)")
    vitamin_c: Optional[float] = Field(alias='vitc', default=None, description="비타민 C(mg)")
    vitamin_d: Optional[float] = Field(alias='vitd', default=None, description="비타민 D(μg)")
    
    # 지방산 및 콜레스테롤
    cholesterol: Optional[float] = Field(alias='chole', default=None, description="콜레스테롤(mg)")
    saturated_fat: Optional[float] = Field(alias='fasat', default=None, description="포화지방산(g)")
    trans_fat: Optional[float] = Field(alias='fatrn', default=None, description="트랜스지방산(g)")
    
    # 기타 정보
    refuse_rate: Optional[float] = Field(alias='refuse', default=None, description="폐기율(%)")
    source_code: Optional[str] = Field(alias='srcCd', default=None, description="출처코드")
    source_name: Optional[str] = Field(alias='srcNm', default=None, description="출처명")
    origin_country_code: Optional[str] = Field(alias='cooCd', default=None, description="원산지국코드")
    origin_country_name: Optional[str] = Field(alias='cooNm', default=None, description="원산지국명")
    is_imported: Optional[str] = Field(alias='imptYn', default=None, description="수입여부")
    
    class Config:
        populate_by_name = True
        json_encoders = {
            float: lambda v: round(v, 2) if v is not None else None
        }


class FoodComposition(BaseModel):
    """음식 구성요소 모델"""
    
    ingredient_name: str = Field(description="재료명")
    percentage: float = Field(description="구성 비율 (0-100%)")
    unit: str = Field(default="g", description="단위")
    
    class Config:
        json_schema_extra = {
            "example": {
                "ingredient_name": "감자",
                "percentage": 60.0,
                "unit": "g"
            }
        }


class ComplexFood(BaseModel):
    """복합식품 모델"""
    
    food_name: str = Field(description="음식명")
    compositions: List[FoodComposition] = Field(description="구성요소 리스트")
    total_weight: float = Field(default=100.0, description="총 중량(g)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "food_name": "감자샐러드",
                "compositions": [
                    {"ingredient_name": "감자", "percentage": 60.0},
                    {"ingredient_name": "마요네즈", "percentage": 25.0},
                    {"ingredient_name": "계란", "percentage": 15.0}
                ],
                "total_weight": 100.0
            }
        }


class NutritionCalculationRequest(BaseModel):
    """영양성분 계산 요청 모델"""
    
    food_name: str = Field(description="음식명")
    weight_grams: float = Field(gt=0, description="중량(g)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "food_name": "감자샐러드",
                "weight_grams": 150.0
            }
        }


class CalculatedNutrition(BaseModel):
    """계산된 영양성분 모델"""
    
    food_name: str = Field(description="음식명")
    weight_grams: float = Field(description="중량(g)")
    
    # 주요 영양성분
    energy: Optional[float] = Field(default=None, description="에너지(kcal)")
    protein: Optional[float] = Field(default=None, description="단백질(g)")
    fat: Optional[float] = Field(default=None, description="지방(g)")
    carbohydrate: Optional[float] = Field(default=None, description="탄수화물(g)")
    sugar: Optional[float] = Field(default=None, description="당류(g)")
    dietary_fiber: Optional[float] = Field(default=None, description="식이섬유(g)")
    
    # 무기질
    calcium: Optional[float] = Field(default=None, description="칼슘(mg)")
    iron: Optional[float] = Field(default=None, description="철(mg)")
    sodium: Optional[float] = Field(default=None, description="나트륨(mg)")
    potassium: Optional[float] = Field(default=None, description="칼륨(mg)")
    
    # 비타민
    vitamin_a: Optional[float] = Field(default=None, description="비타민 A(μg RAE)")
    vitamin_c: Optional[float] = Field(default=None, description="비타민 C(mg)")
    
    # 구성요소별 상세 정보
    composition_details: Optional[List[Dict[str, Any]]] = Field(default=None, description="구성요소별 영양성분")
    
    class Config:
        json_encoders = {
            float: lambda v: round(v, 2) if v is not None else None
        }
        json_schema_extra = {
            "example": {
                "food_name": "감자샐러드",
                "weight_grams": 150.0,
                "energy": 180.5,
                "protein": 3.2,
                "fat": 12.8,
                "carbohydrate": 15.4,
                "sodium": 320.1
            }
        }


class NutritionResponse(BaseModel):
    """영양성분 계산 응답 모델"""
    
    success: bool = Field(description="성공 여부")
    message: str = Field(description="응답 메시지")
    data: Optional[CalculatedNutrition] = Field(default=None, description="계산된 영양성분")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "영양성분 계산이 완료되었습니다.",
                "data": {
                    "food_name": "감자샐러드",
                    "weight_grams": 150.0,
                    "energy": 180.5,
                    "protein": 3.2
                }
            }
        }


class ErrorResponse(BaseModel):
    """에러 응답 모델"""
    
    success: bool = Field(default=False, description="성공 여부")
    error_code: str = Field(description="에러 코드")
    message: str = Field(description="에러 메시지")
    details: Optional[str] = Field(default=None, description="상세 에러 정보")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error_code": "FOOD_NOT_FOUND",
                "message": "해당 음식을 찾을 수 없습니다.",
                "details": "데이터베이스에 '감자샐러드' 정보가 없습니다."
            }
        }