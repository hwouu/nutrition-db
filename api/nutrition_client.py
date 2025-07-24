import os
import requests
import logging
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from .mock_data import get_mock_api_response, get_mock_list_response

# 환경변수 로드
load_dotenv()

logger = logging.getLogger(__name__)


class NutritionAPIClient:
    """공공데이터포털 통합식품영양성분정보 API 클라이언트"""
    
    def __init__(self, use_mock=None):
        self.service_key = os.getenv('SERVICE_KEY')
        self.base_url = os.getenv('API_BASE_URL', 'http://api.data.go.kr/openapi/tn_pubr_public_nutri_material_info_api')
        self.default_num_rows = int(os.getenv('DEFAULT_NUM_OF_ROWS', '100'))
        self.timeout = int(os.getenv('REQUEST_TIMEOUT', '30'))
        
        # Mock 모드 설정 (ENV 변수 또는 인수로 제어)
        if use_mock is None:
            self.use_mock = os.getenv('USE_MOCK_DATA', 'false').lower() == 'true'
        else:
            self.use_mock = use_mock
        
        if not self.use_mock and not self.service_key:
            raise ValueError("SERVICE_KEY 환경변수가 설정되지 않았습니다. 또는 USE_MOCK_DATA=true로 설정하세요.")
    
    def search_food_by_name(self, food_name: str, num_rows: Optional[int] = None) -> Dict[str, Any]:
        """식품명으로 영양성분 정보 검색
        
        Args:
            food_name: 검색할 식품명
            num_rows: 반환할 결과 수 (기본값: 환경변수 값)
            
        Returns:
            API 응답 데이터
        """
        # Mock 모드일 경우 모의 데이터 반환
        if self.use_mock:
            logger.info(f"Mock 모드: '{food_name}' 검색")
            return get_mock_api_response(food_name)
        
        params = {
            'serviceKey': self.service_key,
            'pageNo': '1',
            'numOfRows': str(num_rows or self.default_num_rows),
            'type': 'json',
            'foodNm': food_name
        }
        
        try:
            response = requests.get(
                self.base_url,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            # JSON 응답 파싱
            data = response.json()
            
            # API 에러 체크
            if 'response' in data and 'header' in data['response']:
                header = data['response']['header']
                if header.get('resultCode') != '00':
                    error_msg = f"API 에러: {header.get('resultMsg', '알 수 없는 에러')}"
                    logger.error(error_msg)
                    raise Exception(error_msg)
            
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP 요청 실패: {e}")
            raise
        except Exception as e:
            logger.error(f"API 호출 실패: {e}")
            raise
    
    def search_food_by_code(self, food_code: str) -> Dict[str, Any]:
        """식품코드로 영양성분 정보 검색
        
        Args:
            food_code: 식품코드
            
        Returns:
            API 응답 데이터
        """
        params = {
            'serviceKey': self.service_key,
            'pageNo': '1',
            'numOfRows': '10',
            'type': 'json',
            'foodCd': food_code
        }
        
        try:
            response = requests.get(
                self.base_url,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            
            # API 에러 체크
            if 'header' in data and data['header'].get('resultCode') != '00':
                error_msg = f"API 에러: {data['header'].get('resultMsg', '알 수 없는 에러')}"
                logger.error(error_msg)
                raise Exception(error_msg)
            
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP 요청 실패: {e}")
            raise
        except Exception as e:
            logger.error(f"API 호출 실패: {e}")
            raise
    
    def get_food_list(self, page_no: int = 1, num_rows: int = 100) -> Dict[str, Any]:
        """전체 식품 목록 조회
        
        Args:
            page_no: 페이지 번호
            num_rows: 한 페이지 결과 수
            
        Returns:
            API 응답 데이터
        """
        params = {
            'serviceKey': self.service_key,
            'pageNo': str(page_no),
            'numOfRows': str(num_rows),
            'type': 'json'
        }
        
        try:
            response = requests.get(
                self.base_url,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            
            # API 에러 체크
            if 'header' in data and data['header'].get('resultCode') != '00':
                error_msg = f"API 에러: {data['header'].get('resultMsg', '알 수 없는 에러')}"
                logger.error(error_msg)
                raise Exception(error_msg)
            
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP 요청 실패: {e}")
            raise
        except Exception as e:
            logger.error(f"API 호출 실패: {e}")
            raise
    
    def extract_nutrition_data(self, api_response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """API 응답에서 영양성분 데이터만 추출
        
        Args:
            api_response: API 응답 데이터
            
        Returns:
            영양성분 데이터 리스트
        """
        try:
            # response > body > items 경로에서 데이터 추출
            if 'response' in api_response and 'body' in api_response['response'] and 'items' in api_response['response']['body']:
                return api_response['response']['body']['items']
            else:
                logger.warning("응답에 영양성분 데이터가 없습니다.")
                return []
        except Exception as e:
            logger.error(f"영양성분 데이터 추출 실패: {e}")
            return []