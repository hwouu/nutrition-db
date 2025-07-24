#!/usr/bin/env python3
"""
API 응답 구조 디버깅 스크립트
"""

import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.nutrition_client import NutritionAPIClient


def debug_api_response():
    """API 응답 구조 디버깅"""
    print("=== API 응답 구조 디버깅 ===")
    
    try:
        client = NutritionAPIClient()
        
        # 감자로 검색
        print("'감자' 검색...")
        result = client.search_food_by_name("감자", num_rows=3)
        
        print("전체 응답 구조:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"디버깅 실패: {e}")


def debug_simple_request():
    """단순 요청 디버깅"""
    print("\n=== 단순 요청 디버깅 ===")
    
    try:
        client = NutritionAPIClient()
        
        # 전체 목록 조회
        print("전체 목록 조회...")
        result = client.get_food_list(page_no=1, num_rows=5)
        
        print("전체 목록 응답:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"단순 요청 실패: {e}")


if __name__ == "__main__":
    debug_api_response()
    debug_simple_request()