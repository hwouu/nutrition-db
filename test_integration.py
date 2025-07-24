#!/usr/bin/env python3
"""
통합 테스트 스크립트
FastAPI 서버와 영양성분 계산 기능을 테스트합니다.
"""

import sys
import os
import json
import time
import requests
from concurrent.futures import ThreadPoolExecutor
import subprocess

# 프로젝트 루트를 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.nutrition_service import NutritionCalculationService
from models.schemas import NutritionCalculationRequest


class IntegrationTester:
    """통합 테스트 클래스"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.nutrition_service = NutritionCalculationService()
    
    def test_service_layer(self):
        """서비스 레이어 테스트"""
        print("=== 서비스 레이어 테스트 ===")
        
        try:
            # 1. 사용 가능한 음식 목록 테스트
            foods = self.nutrition_service.get_available_foods()
            print(f"✓ 등록된 음식 수: {len(foods)}")
            print(f"  음식 목록: {', '.join(foods[:5])}...")
            
            # 2. 음식 구성요소 조회 테스트
            if "감자샐러드" in foods:
                composition = self.nutrition_service.get_food_composition("감자샐러드")
                print(f"✓ 감자샐러드 구성요소: {len(composition.compositions)}개")
                for comp in composition.compositions:
                    print(f"  - {comp.ingredient_name}: {comp.percentage}%")
            
            # 3. 영양성분 계산 테스트
            request = NutritionCalculationRequest(
                food_name="감자샐러드",
                weight_grams=150.0
            )
            result = self.nutrition_service.calculate_nutrition(request)
            
            if result:
                print(f"✓ 영양성분 계산 성공:")
                print(f"  - 에너지: {result.energy}kcal")
                print(f"  - 단백질: {result.protein}g")
                print(f"  - 지방: {result.fat}g")
                print(f"  - 탄수화물: {result.carbohydrate}g")
                return True
            else:
                print("✗ 영양성분 계산 실패")
                return False
                
        except Exception as e:
            print(f"✗ 서비스 레이어 테스트 실패: {e}")
            return False
    
    def wait_for_server(self, max_attempts=30):
        """서버가 준비될 때까지 대기"""
        for attempt in range(max_attempts):
            try:
                response = requests.get(f"{self.base_url}/health", timeout=2)
                if response.status_code == 200:
                    print(f"✓ 서버 준비 완료 (시도 {attempt + 1})")
                    return True
            except requests.exceptions.RequestException:
                time.sleep(1)
        
        print(f"✗ 서버 준비 실패 ({max_attempts}초 대기)")
        return False
    
    def test_api_endpoints(self):
        """API 엔드포인트 테스트"""
        print("\\n=== API 엔드포인트 테스트 ===")
        
        if not self.wait_for_server():
            return False
        
        tests_passed = 0
        total_tests = 0
        
        # 1. 루트 엔드포인트 테스트
        total_tests += 1
        try:
            response = requests.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                print(f"✓ 루트 엔드포인트: {data['service']}")
                tests_passed += 1
            else:
                print(f"✗ 루트 엔드포인트 실패: {response.status_code}")
        except Exception as e:
            print(f"✗ 루트 엔드포인트 오류: {e}")
        
        # 2. 헬스체크 테스트
        total_tests += 1
        try:
            response = requests.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✓ 헬스체크: {data['status']}")
                tests_passed += 1
            else:
                print(f"✗ 헬스체크 실패: {response.status_code}")
        except Exception as e:
            print(f"✗ 헬스체크 오류: {e}")
        
        # 3. 음식 목록 조회 테스트
        total_tests += 1
        try:
            response = requests.get(f"{self.base_url}/foods")
            if response.status_code == 200:
                foods = response.json()
                print(f"✓ 음식 목록: {len(foods)}개")
                tests_passed += 1
            else:
                print(f"✗ 음식 목록 실패: {response.status_code}")
        except Exception as e:
            print(f"✗ 음식 목록 오류: {e}")
        
        # 4. 음식 구성요소 조회 테스트
        total_tests += 1
        try:
            response = requests.get(f"{self.base_url}/foods/감자샐러드")
            if response.status_code == 200:
                data = response.json()
                print(f"✓ 음식 구성요소: {data['food_name']}")
                tests_passed += 1
            else:
                print(f"✗ 음식 구성요소 실패: {response.status_code}")
        except Exception as e:
            print(f"✗ 음식 구성요소 오류: {e}")
        
        # 5. 영양성분 계산 테스트 (POST)
        total_tests += 1
        try:
            payload = {
                "food_name": "감자샐러드",
                "weight_grams": 150.0
            }
            response = requests.post(
                f"{self.base_url}/calculate-nutrition",
                json=payload
            )
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    nutrition = data['data']
                    print(f"✓ 영양성분 계산 (POST): {nutrition['energy']}kcal")
                    tests_passed += 1
                else:
                    print(f"✗ 영양성분 계산 실패: {data['message']}")
            else:
                print(f"✗ 영양성분 계산 실패: {response.status_code}")
        except Exception as e:
            print(f"✗ 영양성분 계산 오류: {e}")
        
        # 6. 영양성분 계산 테스트 (GET)
        total_tests += 1
        try:
            response = requests.get(f"{self.base_url}/calculate-nutrition/감자샐러드/100")
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    nutrition = data['data']
                    print(f"✓ 영양성분 계산 (GET): {nutrition['energy']}kcal")
                    tests_passed += 1
                else:
                    print(f"✗ 영양성분 계산 실패: {data['message']}")
            else:
                print(f"✗ 영양성분 계산 실패: {response.status_code}")
        except Exception as e:
            print(f"✗ 영양성분 계산 오류: {e}")
        
        print(f"\\nAPI 테스트 결과: {tests_passed}/{total_tests} 통과")
        return tests_passed == total_tests
    
    def test_multiple_foods(self):
        """여러 음식 동시 테스트"""
        print("\\n=== 여러 음식 동시 테스트 ===")
        
        foods_to_test = [
            ("감자샐러드", 150),
            ("야채샐러드", 100),
            ("계란프라이", 80),
            ("감자튀김", 120)
        ]
        
        def test_single_food(food_data):
            food_name, weight = food_data
            try:
                response = requests.get(
                    f"{self.base_url}/calculate-nutrition/{food_name}/{weight}",
                    timeout=10
                )
                if response.status_code == 200:
                    data = response.json()
                    if data['success']:
                        nutrition = data['data']
                        return f"✓ {food_name}({weight}g): {nutrition['energy']}kcal"
                    else:
                        return f"✗ {food_name}: {data['message']}"
                else:
                    return f"✗ {food_name}: HTTP {response.status_code}"
            except Exception as e:
                return f"✗ {food_name}: {e}"
        
        # 병렬로 테스트 실행
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(test_single_food, foods_to_test))
        
        for result in results:
            print(f"  {result}")
        
        success_count = sum(1 for result in results if result.startswith("✓"))
        print(f"\\n동시 테스트 결과: {success_count}/{len(foods_to_test)} 성공")
        
        return success_count == len(foods_to_test)


def main():
    """메인 테스트 함수"""
    print("통합 테스트 시작")
    print("=" * 60)
    
    tester = IntegrationTester()
    
    # 1. 서비스 레이어 테스트
    service_test_passed = tester.test_service_layer()
    
    # 2. FastAPI 서버 시작
    print("\\n=== FastAPI 서버 시작 ===")
    print("서버를 시작합니다...")
    print("테스트 완료 후 Ctrl+C로 서버를 종료하세요.")
    
    # 서버를 백그라운드에서 시작
    server_process = None
    try:
        server_process = subprocess.Popen([
            sys.executable, "main.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 3. API 엔드포인트 테스트
        api_test_passed = tester.test_api_endpoints()
        
        # 4. 여러 음식 동시 테스트
        concurrent_test_passed = tester.test_multiple_foods()
        
        # 결과 요약
        print("\\n" + "=" * 60)
        print("통합 테스트 결과 요약:")
        print(f"  1. 서비스 레이어: {'✓ 통과' if service_test_passed else '✗ 실패'}")
        print(f"  2. API 엔드포인트: {'✓ 통과' if api_test_passed else '✗ 실패'}")
        print(f"  3. 동시 처리: {'✓ 통과' if concurrent_test_passed else '✗ 실패'}")
        
        all_passed = service_test_passed and api_test_passed and concurrent_test_passed
        
        if all_passed:
            print("\\n🎉 모든 테스트가 성공했습니다!")
            print(f"\\n✅ API 서버가 정상적으로 작동 중입니다:")
            print(f"   - 서버 주소: http://localhost:8000")
            print(f"   - API 문서: http://localhost:8000/docs")
            curl_example = 'curl -X POST http://localhost:8000/calculate-nutrition -H "Content-Type: application/json" -d \'{"food_name": "감자샐러드", "weight_grams": 150}\''
            print(f"   - 예시 요청: {curl_example}")
        else:
            print("\\n⚠️ 일부 테스트가 실패했습니다.")
        
        return all_passed
        
    except KeyboardInterrupt:
        print("\\n테스트가 중단되었습니다.")
        return False
    finally:
        if server_process:
            server_process.terminate()
            server_process.wait()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)