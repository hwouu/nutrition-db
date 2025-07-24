import axios from 'axios';
import type { 
  NutritionResponse, 
  NutritionCalculationRequest, 
  ComplexFood 
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Response Error:', error);
    if (error.response?.status === 404) {
      throw new Error('해당 음식을 찾을 수 없습니다.');
    } else if (error.response?.status >= 500) {
      throw new Error('서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
    } else if (error.code === 'ECONNABORTED') {
      throw new Error('요청 시간이 초과되었습니다.');
    }
    throw error;
  }
);

export const nutritionApi = {
  // 헬스체크
  async healthCheck() {
    const response = await apiClient.get('/health');
    return response.data;
  },

  // 등록된 음식 목록 조회
  async getFoodList(): Promise<string[]> {
    const response = await apiClient.get('/foods');
    return response.data;
  },

  // 특정 음식의 구성요소 정보 조회
  async getFoodComposition(foodName: string): Promise<ComplexFood> {
    const response = await apiClient.get(`/foods/${encodeURIComponent(foodName)}`);
    return response.data;
  },

  // 영양성분 계산 (POST)
  async calculateNutrition(request: NutritionCalculationRequest): Promise<NutritionResponse> {
    const response = await apiClient.post('/calculate-nutrition', request);
    return response.data;
  },

  // 영양성분 계산 (GET - 간편 방식)
  async calculateNutritionSimple(foodName: string, weight: number): Promise<NutritionResponse> {
    const response = await apiClient.get(
      `/calculate-nutrition/${encodeURIComponent(foodName)}/${weight}`
    );
    return response.data;
  },

  // 개별 재료의 영양성분 정보 조회
  async getIngredientNutrition(ingredientName: string) {
    const response = await apiClient.get(`/ingredients/${encodeURIComponent(ingredientName)}`);
    return response.data;
  },
};

export default apiClient;