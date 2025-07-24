"""
개발용 모의 데이터
실제 API 연결이 어려울 때 사용하는 샘플 데이터
"""

MOCK_NUTRITION_DATA = {
    "감자": {
        "foodCd": "01001001",
        "foodNm": "감자, 생것",
        "enerc": 77.0,
        "water": 78.9,
        "prot": 2.0,
        "fatce": 0.1,
        "ash": 1.0,
        "chocdf": 18.0,
        "sugar": 1.2,
        "fibtg": 2.0,
        "ca": 6.0,
        "fe": 0.6,
        "p": 44.0,
        "k": 421.0,
        "nat": 4.0,
        "vitaRae": 1.0,
        "retol": 0.0,
        "cartb": 6.0,
        "thia": 0.08,
        "ribf": 0.03,
        "nia": 1.0,
        "vitc": 20.0,
        "vitd": 0.0,
        "chole": 0.0,
        "fasat": 0.03,
        "fatrn": 0.0,
        "refuse": 15.0,
        "srcCd": "01",
        "srcNm": "농촌진흥청"
    },
    "계란": {
        "foodCd": "02002001",
        "foodNm": "계란, 전란, 생것",
        "enerc": 143.0,
        "water": 76.2,
        "prot": 12.6,
        "fatce": 9.9,
        "ash": 1.0,
        "chocdf": 0.3,
        "sugar": 0.2,
        "fibtg": 0.0,
        "ca": 52.0,
        "fe": 1.8,
        "p": 180.0,
        "k": 138.0,
        "nat": 124.0,
        "vitaRae": 140.0,
        "retol": 140.0,
        "cartb": 0.0,
        "thia": 0.10,
        "ribf": 0.45,
        "nia": 0.1,
        "vitc": 0.0,
        "vitd": 1.1,
        "chole": 372.0,
        "fasat": 3.1,
        "fatrn": 0.03,
        "refuse": 12.0,
        "srcCd": "01",
        "srcNm": "농촌진흥청"
    },
    "마요네즈": {
        "foodCd": "03003001",
        "foodNm": "마요네즈",
        "enerc": 680.0,
        "water": 15.8,
        "prot": 1.3,
        "fatce": 75.0,
        "ash": 1.5,
        "chocdf": 6.4,
        "sugar": 2.1,
        "fibtg": 0.0,
        "ca": 19.0,
        "fe": 0.5,
        "p": 46.0,
        "k": 37.0,
        "nat": 506.0,
        "vitaRae": 85.0,
        "retol": 0.0,
        "cartb": 0.0,
        "thia": 0.01,
        "ribf": 0.04,
        "nia": 0.1,
        "vitc": 0.0,
        "vitd": 0.0,
        "chole": 59.0,
        "fasat": 11.2,
        "fatrn": 0.2,
        "refuse": 0.0,
        "srcCd": "01",
        "srcNm": "농촌진흥청"
    },
    "양파": {
        "foodCd": "04004001",
        "foodNm": "양파, 생것",
        "enerc": 40.0,
        "water": 89.0,
        "prot": 1.1,
        "fatce": 0.1,
        "ash": 0.4,
        "chocdf": 9.4,
        "sugar": 4.2,
        "fibtg": 1.8,
        "ca": 23.0,
        "fe": 0.2,
        "p": 29.0,
        "k": 146.0,
        "nat": 4.0,
        "vitaRae": 1.0,
        "retol": 0.0,
        "cartb": 6.0,
        "thia": 0.03,
        "ribf": 0.03,
        "nia": 0.1,
        "vitc": 8.0,
        "vitd": 0.0,
        "chole": 0.0,
        "fasat": 0.03,
        "fatrn": 0.0,
        "refuse": 10.0,
        "srcCd": "01",
        "srcNm": "농촌진흥청"
    },
    "당근": {
        "foodCd": "05005001",
        "foodNm": "당근, 생것",
        "enerc": 41.0,
        "water": 88.3,
        "prot": 0.9,
        "fatce": 0.2,
        "ash": 1.0,
        "chocdf": 9.6,
        "sugar": 4.7,
        "fibtg": 2.8,
        "ca": 33.0,
        "fe": 0.3,
        "p": 35.0,
        "k": 320.0,
        "nat": 69.0,
        "vitaRae": 835.0,
        "retol": 0.0,
        "cartb": 8285.0,
        "thia": 0.06,
        "ribf": 0.06,
        "nia": 0.6,
        "vitc": 6.0,
        "vitd": 0.0,
        "chole": 0.0,
        "fasat": 0.04,
        "fatrn": 0.0,
        "refuse": 10.0,
        "srcCd": "01",
        "srcNm": "농촌진흥청"
    }
}


def get_mock_api_response(food_name: str):
    """모의 API 응답 생성"""
    if food_name in MOCK_NUTRITION_DATA:
        return {
            "response": {
                "header": {
                    "resultCode": "00",
                    "resultMsg": "NORMAL SERVICE."
                },
                "body": {
                    "totalCount": 1,
                    "items": [MOCK_NUTRITION_DATA[food_name]]
                }
            }
        }
    else:
        return {
            "response": {
                "header": {
                    "resultCode": "03",
                    "resultMsg": "NODATA_ERROR"
                },
                "body": {
                    "totalCount": 0,
                    "items": []
                }
            }
        }


def get_mock_list_response():
    """모의 목록 API 응답 생성"""
    items = list(MOCK_NUTRITION_DATA.values())
    return {
        "response": {
            "header": {
                "resultCode": "00",
                "resultMsg": "NORMAL SERVICE."
            },
            "body": {
                "totalCount": len(items),
                "items": items
            }
        }
    }