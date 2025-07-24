import json
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

from api.nutrition_client import NutritionAPIClient
from models.schemas import (
    NutritionInfo, 
    ComplexFood, 
    FoodComposition, 
    CalculatedNutrition,
    NutritionCalculationRequest
)

logger = logging.getLogger(__name__)


class NutritionCalculationService:
    """영양성분 계산 서비스"""
    
    def __init__(self, use_mock=None):
        self.api_client = NutritionAPIClient(use_mock=use_mock)
        self.compositions_file = Path(__file__).parent.parent / "data" / "food_compositions.json"
        self.food_compositions = self._load_food_compositions()
    
    def _load_food_compositions(self) -> Dict[str, Any]:
        """음식 구성요소 데이터 로드"""
        try:
            with open(self.compositions_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"구성요소 데이터 파일을 찾을 수 없습니다: {self.compositions_file}")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"구성요소 데이터 파싱 실패: {e}")
            return {}
    
    def get_available_foods(self) -> List[str]:
        """등록된 복합식품 목록 반환"""
        return list(self.food_compositions.keys())
    
    def get_food_composition(self, food_name: str) -> Optional[ComplexFood]:
        """특정 음식의 구성요소 정보 반환"""
        if food_name not in self.food_compositions:
            return None
        
        composition_data = self.food_compositions[food_name]
        
        # FoodComposition 객체 리스트 생성
        compositions = []
        for comp in composition_data['compositions']:
            compositions.append(FoodComposition(
                ingredient_name=comp['ingredient_name'],
                percentage=comp['percentage'],
                unit=comp.get('unit', 'g')
            ))
        
        return ComplexFood(
            food_name=food_name,
            compositions=compositions,
            total_weight=composition_data.get('base_weight', 100.0)
        )
    
    def get_ingredient_nutrition(self, ingredient_name: str) -> Optional[NutritionInfo]:
        """개별 재료의 영양성분 정보 조회"""
        try:
            # API에서 해당 재료의 영양성분 조회
            response = self.api_client.search_food_by_name(ingredient_name, num_rows=1)
            nutrition_data = self.api_client.extract_nutrition_data(response)
            
            if not nutrition_data:
                logger.warning(f"'{ingredient_name}' 영양성분 정보를 찾을 수 없습니다.")
                return None
            
            # 첫 번째 결과 사용
            first_result = nutrition_data[0]
            
            # NutritionInfo 객체 생성
            nutrition_info = NutritionInfo(**first_result)
            return nutrition_info
            
        except Exception as e:
            logger.error(f"'{ingredient_name}' 영양성분 조회 실패: {e}")
            return None
    
    def calculate_nutrition(self, request: NutritionCalculationRequest) -> Optional[CalculatedNutrition]:
        """영양성분 계산 메인 메소드"""
        food_name = request.food_name
        target_weight = request.weight_grams
        
        # 1. 음식 구성요소 정보 조회
        complex_food = self.get_food_composition(food_name)
        if not complex_food:
            logger.error(f"'{food_name}' 구성요소 정보를 찾을 수 없습니다.")
            return None
        
        # 2. 각 구성요소별 영양성분 조회 및 계산
        total_nutrition = {
            'energy': 0.0,
            'protein': 0.0,
            'fat': 0.0,
            'carbohydrate': 0.0,
            'sugar': 0.0,
            'dietary_fiber': 0.0,
            'calcium': 0.0,
            'iron': 0.0,
            'sodium': 0.0,
            'potassium': 0.0,
            'vitamin_a': 0.0,
            'vitamin_c': 0.0
        }
        
        composition_details = []
        
        # 기준 중량 대비 실제 요청 중량의 비율 계산
        weight_ratio = target_weight / complex_food.total_weight
        
        for composition in complex_food.compositions:
            ingredient_name = composition.ingredient_name
            percentage = composition.percentage
            
            # 해당 재료의 영양성분 조회
            nutrition = self.get_ingredient_nutrition(ingredient_name)
            if not nutrition:
                logger.warning(f"'{ingredient_name}' 영양성분을 건너뜁니다.")
                continue
            
            # 실제 사용량 계산 (목표 중량 * 구성 비율 / 100)
            actual_weight = target_weight * (percentage / 100.0)
            
            # 영양성분 계산 (100g 기준 → 실제 사용량 기준)
            nutrition_ratio = actual_weight / 100.0
            
            ingredient_nutrition = {
                'ingredient_name': ingredient_name,
                'weight': actual_weight,
                'energy': (nutrition.energy or 0) * nutrition_ratio,
                'protein': (nutrition.protein or 0) * nutrition_ratio,
                'fat': (nutrition.fat or 0) * nutrition_ratio,
                'carbohydrate': (nutrition.carbohydrate or 0) * nutrition_ratio,
                'sugar': (nutrition.sugar or 0) * nutrition_ratio,
                'dietary_fiber': (nutrition.dietary_fiber or 0) * nutrition_ratio,
                'calcium': (nutrition.calcium or 0) * nutrition_ratio,
                'iron': (nutrition.iron or 0) * nutrition_ratio,
                'sodium': (nutrition.sodium or 0) * nutrition_ratio,
                'potassium': (nutrition.potassium or 0) * nutrition_ratio,
                'vitamin_a': (nutrition.vitamin_a or 0) * nutrition_ratio,
                'vitamin_c': (nutrition.vitamin_c or 0) * nutrition_ratio
            }
            
            composition_details.append(ingredient_nutrition)
            
            # 총합에 추가
            for key in total_nutrition:
                if key in ingredient_nutrition:
                    total_nutrition[key] += ingredient_nutrition[key]
        
        # 3. 최종 결과 생성
        calculated_nutrition = CalculatedNutrition(
            food_name=food_name,
            weight_grams=target_weight,
            energy=round(total_nutrition['energy'], 2),
            protein=round(total_nutrition['protein'], 2),
            fat=round(total_nutrition['fat'], 2),
            carbohydrate=round(total_nutrition['carbohydrate'], 2),
            sugar=round(total_nutrition['sugar'], 2),
            dietary_fiber=round(total_nutrition['dietary_fiber'], 2),
            calcium=round(total_nutrition['calcium'], 2),
            iron=round(total_nutrition['iron'], 2),
            sodium=round(total_nutrition['sodium'], 2),
            potassium=round(total_nutrition['potassium'], 2),
            vitamin_a=round(total_nutrition['vitamin_a'], 2),
            vitamin_c=round(total_nutrition['vitamin_c'], 2),
            composition_details=composition_details
        )
        
        return calculated_nutrition
    
    def get_nutrition_summary(self, food_name: str, weight_grams: float) -> Dict[str, Any]:
        """영양성분 요약 정보 반환"""
        request = NutritionCalculationRequest(
            food_name=food_name,
            weight_grams=weight_grams
        )
        
        result = self.calculate_nutrition(request)
        if not result:
            return {
                "success": False,
                "message": f"'{food_name}' 영양성분 계산에 실패했습니다.",
                "data": None
            }
        
        return {
            "success": True,
            "message": "영양성분 계산이 완료되었습니다.",
            "data": result.model_dump()
        }