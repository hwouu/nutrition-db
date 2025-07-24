#!/usr/bin/env python3
"""
공공데이터 API 연결 테스트 스크립트
"""

import sys
import os
import json

# 프로젝트 루트를 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.nutrition_client import NutritionAPIClient


def test_basic_connection():
    """기본 연결 테스트"""
    print("=== 기본 연결 테스트 ===")
    
    try:
        client = NutritionAPIClient()
        print(f"✓ 클라이언트 초기화 성공")
        print(f"  - API URL: {client.base_url}")
        print(f"  - 서비스키: {client.service_key[:20]}...")
        return True
    except Exception as e:
        print(f"✗ 클라이언트 초기화 실패: {e}")
        return False


def test_search_by_name():
    """식품명 검색 테스트"""
    print("\n=== 식품명 검색 테스트 ===")
    
    try:
        client = NutritionAPIClient()
        
        # 감자로 검색
        print("'감자' 검색 중...")
        result = client.search_food_by_name("감자", num_rows=5)
        
        print(f"✓ API 호출 성공")
        
        # 응답 구조 확인
        if 'header' in result:
            header = result['header']
            print(f"  - 응답 코드: {header.get('resultCode')}")
            print(f"  - 응답 메시지: {header.get('resultMsg')}")
        
        if 'body' in result:
            body = result['body']
            total_count = body.get('totalCount', 0)
            print(f"  - 총 결과 수: {total_count}")
            
            if 'items' in body and body['items']:
                items = body['items']
                print(f"  - 반환된 항목 수: {len(items)}")
                
                # 첫 번째 항목 상세 정보
                first_item = items[0]
                print(f"  - 첫 번째 항목:")
                print(f"    식품코드: {first_item.get('foodCd')}")
                print(f"    식품명: {first_item.get('foodNm')}")
                print(f"    에너지: {first_item.get('enerc')} kcal")
                print(f"    단백질: {first_item.get('prot')} g")
                print(f"    지방: {first_item.get('fatce')} g")
                print(f"    탄수화물: {first_item.get('chocdf')} g")
                
                return True
            else:
                print("  - 검색 결과가 없습니다.")
                return False
        
    except Exception as e:
        print(f"✗ 식품명 검색 실패: {e}")
        return False


def test_nutrition_data_extraction():
    """영양성분 데이터 추출 테스트"""
    print("\n=== 영양성분 데이터 추출 테스트 ===")
    
    try:
        client = NutritionAPIClient()
        
        # 계란으로 검색
        print("'계란' 검색 중...")
        result = client.search_food_by_name("계란", num_rows=3)
        
        # 영양성분 데이터 추출
        nutrition_data = client.extract_nutrition_data(result)
        
        print(f"✓ 영양성분 데이터 추출 성공")
        print(f"  - 추출된 항목 수: {len(nutrition_data)}")
        
        if nutrition_data:
            for i, item in enumerate(nutrition_data):
                print(f"  - 항목 {i+1}:")
                print(f"    식품명: {item.get('foodNm')}")
                print(f"    에너지: {item.get('enerc')} kcal")
                print(f"    출처: {item.get('srcNm')}")
        
        return True
        
    except Exception as e:
        print(f"✗ 영양성분 데이터 추출 실패: {e}")
        return False


def test_multiple_searches():
    """여러 식품 검색 테스트"""
    print("\n=== 여러 식품 검색 테스트 ===")
    
    foods = ["마요네즈", "양파", "당근"]
    
    try:
        client = NutritionAPIClient()
        results = {}
        
        for food in foods:
            print(f"'{food}' 검색 중...")
            result = client.search_food_by_name(food, num_rows=1)
            nutrition_data = client.extract_nutrition_data(result)
            
            if nutrition_data:
                results[food] = nutrition_data[0]
                print(f"  ✓ {food}: {nutrition_data[0].get('foodNm')}")
            else:
                print(f"  ✗ {food}: 검색 결과 없음")
        
        print(f"\n총 {len(results)}개 식품 검색 성공:")
        for food, data in results.items():
            print(f"  - {food}: {data.get('enerc')} kcal")
        
        return len(results) > 0
        
    except Exception as e:
        print(f"✗ 여러 식품 검색 실패: {e}")
        return False


def main():
    """메인 테스트 함수"""
    print("공공데이터 API 연결 테스트 시작")
    print("=" * 50)
    
    tests = [
        test_basic_connection,
        test_search_by_name,
        test_nutrition_data_extraction,
        test_multiple_searches
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"테스트 실행 중 오류: {e}")
    
    print("\n" + "=" * 50)
    print(f"테스트 결과: {passed}/{total} 통과")
    
    if passed == total:
        print("🎉 모든 테스트가 성공했습니다!")
        return True
    else:
        print("⚠️ 일부 테스트가 실패했습니다.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)