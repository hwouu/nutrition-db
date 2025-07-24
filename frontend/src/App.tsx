import { useState, useEffect } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import axios from 'axios';
import { Search, Calculator, Info, ChevronDown, ChevronUp } from 'lucide-react';

const queryClient = new QueryClient();

interface NutritionData {
  food_name: string;
  weight_grams: number;
  energy: number;
  protein: number;
  fat: number;
  carbohydrate: number;
  sugar: number;
  dietary_fiber: number;
  calcium: number;
  iron: number;
  sodium: number;
  potassium: number;
  vitamin_a: number;
  vitamin_c: number;
  composition_details: Array<{
    ingredient_name: string;
    weight: number;
    energy: number;
    protein: number;
    fat: number;
    carbohydrate: number;
    sugar: number;
    dietary_fiber: number;
    calcium: number;
    iron: number;
    sodium: number;
    potassium: number;
    vitamin_a: number;
    vitamin_c: number;
  }>;
}

interface FoodComposition {
  food_name: string;
  compositions: Array<{
    ingredient_name: string;
    percentage: number;
    unit: string;
  }>;
  total_weight: number;
}

interface SavedNutrition {
  id: string;
  timestamp: string;
  data: NutritionData;
}

function NutritionCalculator() {
  const [foodName, setFoodName] = useState('');
  const [weight, setWeight] = useState<number>(100);
  const [loading, setLoading] = useState(false);
  const [nutritionData, setNutritionData] = useState<NutritionData | null>(null);
  const [foodComposition, setFoodComposition] = useState<FoodComposition | null>(null);
  const [availableFoods, setAvailableFoods] = useState<string[]>([]);
  const [savedResults, setSavedResults] = useState<SavedNutrition[]>([]);
  const [error, setError] = useState<string>('');
  const [showSavedResults, setShowSavedResults] = useState(false);
  const [showIngredientDetails, setShowIngredientDetails] = useState(false);

  // 페이지 로드 시 사용 가능한 음식 목록 가져오기
  const fetchAvailableFoods = async () => {
    try {
      const response = await axios.get('http://localhost:8000/foods');
      setAvailableFoods(response.data);
    } catch (error) {
      console.error('음식 목록 가져오기 실패:', error);
    }
  };

  // 영양성분 계산
  const calculateNutrition = async () => {
    if (!foodName.trim()) {
      setError('음식 이름을 입력해주세요.');
      return;
    }
    if (weight <= 0) {
      setError('중량은 0보다 큰 값을 입력해주세요.');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      // 영양성분 계산
      const nutritionResponse = await axios.post('http://localhost:8000/calculate-nutrition', {
        food_name: foodName,
        weight_grams: weight
      });

      if (!nutritionResponse.data.success) {
        setError(nutritionResponse.data.message);
        return;
      }

      const nutrition = nutritionResponse.data.data;
      setNutritionData(nutrition);

      // 음식 구성 정보 가져오기
      try {
        const compositionResponse = await axios.get(`http://localhost:8000/foods/${foodName}`);
        setFoodComposition(compositionResponse.data);
      } catch (compositionError) {
        console.log('음식 구성 정보 없음 (단일 재료일 수 있음)');
        setFoodComposition(null);
      }

      // 결과 저장 (로컬 스토리지 활용)
      const savedResult: SavedNutrition = {
        id: Date.now().toString(),
        timestamp: new Date().toLocaleString('ko-KR'),
        data: nutrition
      };
      
      const existingSaved = JSON.parse(localStorage.getItem('savedNutrition') || '[]');
      const updatedSaved = [savedResult, ...existingSaved].slice(0, 10); // 최대 10개 저장
      localStorage.setItem('savedNutrition', JSON.stringify(updatedSaved));
      setSavedResults(updatedSaved);

    } catch (error: any) {
      if (error.response?.status === 404) {
        setError(`'${foodName}' 음식을 찾을 수 없습니다. 사용 가능한 음식 목록을 확인해주세요.`);
      } else {
        setError('영양성분 계산 중 오류가 발생했습니다.');
      }
      console.error('영양성분 계산 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  // 저장된 결과 불러오기
  const loadSavedResults = () => {
    const saved = JSON.parse(localStorage.getItem('savedNutrition') || '[]');
    setSavedResults(saved);
    setShowSavedResults(!showSavedResults);
  };

  // 페이지 로드 시 초기화
  useEffect(() => {
    fetchAvailableFoods();
    const saved = JSON.parse(localStorage.getItem('savedNutrition') || '[]');
    setSavedResults(saved);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <div className="flex items-center space-x-3">
            <Calculator className="h-8 w-8 text-primary-600" />
            <div>
              <h1 className="text-2xl font-bold text-gray-900">영양성분 계산기</h1>
              <p className="text-sm text-gray-600">한국 공공데이터 기반 통합식품 영양성분 분석</p>
            </div>
          </div>
        </div>
      </header>

      <div className="flex-1">
        <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
        {/* 입력 폼 */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            <Search className="inline h-5 w-5 mr-2" />
            영양성분 계산
          </h2>
          
          <div className="grid md:grid-cols-3 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                음식 이름
              </label>
              <input
                type="text"
                value={foodName}
                onChange={(e) => setFoodName(e.target.value)}
                placeholder="예: 감자샐러드"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                중량 (g)
              </label>
              <input
                type="number"
                value={weight}
                onChange={(e) => setWeight(Number(e.target.value))}
                min="1"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>
            <div className="flex items-end">
              <button
                onClick={calculateNutrition}
                disabled={loading}
                className="w-full bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? '계산 중...' : '계산하기'}
              </button>
            </div>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-md p-3 mb-4">
              <p className="text-red-800 text-sm">{error}</p>
            </div>
          )}

          {/* 사용 가능한 음식 목록 */}
          {availableFoods.length > 0 && (
            <div className="bg-blue-50 rounded-md p-4">
              <p className="text-sm font-medium text-blue-900 mb-2">사용 가능한 음식:</p>
              <div className="flex flex-wrap gap-2">
                {availableFoods.map(food => (
                  <button
                    key={food}
                    onClick={() => setFoodName(food)}
                    className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm hover:bg-blue-200 transition-colors"
                  >
                    {food}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* 영양성분 결과 */}
        {nutritionData && (
          <>
            {/* 기본 영양성분 */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                영양성분 정보 ({nutritionData.food_name} {nutritionData.weight_grams}g)
              </h3>
              
              <div className="grid md:grid-cols-4 gap-4 mb-6">
                <div className="bg-red-50 rounded-lg p-4 text-center">
                  <div className="text-2xl font-bold text-red-600">{nutritionData.energy.toFixed(1)}</div>
                  <div className="text-sm text-red-800">칼로리 (kcal)</div>
                </div>
                <div className="bg-blue-50 rounded-lg p-4 text-center">
                  <div className="text-2xl font-bold text-blue-600">{nutritionData.protein.toFixed(1)}</div>
                  <div className="text-sm text-blue-800">단백질 (g)</div>
                </div>
                <div className="bg-yellow-50 rounded-lg p-4 text-center">
                  <div className="text-2xl font-bold text-yellow-600">{nutritionData.carbohydrate.toFixed(1)}</div>
                  <div className="text-sm text-yellow-800">탄수화물 (g)</div>
                </div>
                <div className="bg-green-50 rounded-lg p-4 text-center">
                  <div className="text-2xl font-bold text-green-600">{nutritionData.fat.toFixed(1)}</div>
                  <div className="text-sm text-green-800">지방 (g)</div>
                </div>
              </div>

              {/* 상세 영양성분 */}
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-medium text-gray-900 mb-3">미네랄</h4>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-gray-600">칼슘</span>
                      <span className="font-medium">{nutritionData.calcium.toFixed(1)} mg</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">철분</span>
                      <span className="font-medium">{nutritionData.iron.toFixed(1)} mg</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">나트륨</span>
                      <span className="font-medium">{nutritionData.sodium.toFixed(1)} mg</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">칼륨</span>
                      <span className="font-medium">{nutritionData.potassium.toFixed(1)} mg</span>
                    </div>
                  </div>
                </div>
                <div>
                  <h4 className="font-medium text-gray-900 mb-3">비타민 & 기타</h4>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-gray-600">비타민 A</span>
                      <span className="font-medium">{nutritionData.vitamin_a.toFixed(1)} μg</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">비타민 C</span>
                      <span className="font-medium">{nutritionData.vitamin_c.toFixed(1)} mg</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">당류</span>
                      <span className="font-medium">{nutritionData.sugar.toFixed(1)} g</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">식이섬유</span>
                      <span className="font-medium">{nutritionData.dietary_fiber.toFixed(1)} g</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* 원재료 구성 정보 */}
            {foodComposition && (
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">원재료 구성</h3>
                  <button
                    onClick={() => setShowIngredientDetails(!showIngredientDetails)}
                    className="flex items-center text-primary-600 hover:text-primary-700"
                  >
                    상세보기
                    {showIngredientDetails ? <ChevronUp className="h-4 w-4 ml-1" /> : <ChevronDown className="h-4 w-4 ml-1" />}
                  </button>
                </div>
                
                <div className="grid md:grid-cols-3 gap-4 mb-4">
                  {foodComposition.compositions.map((comp, index) => (
                    <div key={index} className="bg-gray-50 rounded-lg p-4">
                      <div className="font-medium text-gray-900">{comp.ingredient_name}</div>
                      <div className="text-2xl font-bold text-primary-600">{comp.percentage}%</div>
                      <div className="text-sm text-gray-600">{(weight * comp.percentage / 100).toFixed(1)}g</div>
                    </div>
                  ))}
                </div>

                {showIngredientDetails && nutritionData.composition_details && (
                  <div className="border-t pt-4">
                    <h4 className="font-medium text-gray-900 mb-3">재료별 영양성분</h4>
                    <div className="overflow-x-auto">
                      <table className="min-w-full">
                        <thead className="bg-gray-50">
                          <tr>
                            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">재료</th>
                            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">중량(g)</th>
                            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">칼로리</th>
                            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">단백질</th>
                            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">탄수화물</th>
                            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">지방</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200">
                          {nutritionData.composition_details.map((detail, index) => (
                            <tr key={index}>
                              <td className="px-4 py-2 font-medium text-gray-900">{detail.ingredient_name}</td>
                              <td className="px-4 py-2 text-gray-600">{detail.weight.toFixed(1)}</td>
                              <td className="px-4 py-2 text-gray-600">{detail.energy.toFixed(1)}</td>
                              <td className="px-4 py-2 text-gray-600">{detail.protein.toFixed(1)}g</td>
                              <td className="px-4 py-2 text-gray-600">{detail.carbohydrate.toFixed(1)}g</td>
                              <td className="px-4 py-2 text-gray-600">{detail.fat.toFixed(1)}g</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}
              </div>
            )}
          </>
        )}

        {/* 저장된 결과 */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">계산 기록</h3>
            <button
              onClick={loadSavedResults}
              className="flex items-center text-primary-600 hover:text-primary-700"
            >
              {showSavedResults ? '숨기기' : '보기'}
              {showSavedResults ? <ChevronUp className="h-4 w-4 ml-1" /> : <ChevronDown className="h-4 w-4 ml-1" />}
            </button>
          </div>

          {showSavedResults && savedResults.length > 0 && (
            <div className="space-y-3">
              {savedResults.map((result) => (
                <div key={result.id} className="bg-gray-50 rounded-lg p-4">
                  <div className="flex justify-between items-start">
                    <div>
                      <div className="font-medium text-gray-900">
                        {result.data.food_name} ({result.data.weight_grams}g)
                      </div>
                      <div className="text-sm text-gray-600">{result.timestamp}</div>
                    </div>
                    <div className="text-right">
                      <div className="font-bold text-red-600">{result.data.energy.toFixed(1)} kcal</div>
                      <div className="text-xs text-gray-500">
                        P:{result.data.protein.toFixed(1)}g C:{result.data.carbohydrate.toFixed(1)}g F:{result.data.fat.toFixed(1)}g
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {showSavedResults && savedResults.length === 0 && (
            <p className="text-gray-500 text-center py-4">저장된 계산 기록이 없습니다.</p>
          )}
        </div>
        </div>
      </div>

      {/* Footer - 데이터 출처 */}
      <footer className="bg-gray-800 text-white py-4 mt-auto">
        <div className="max-w-4xl mx-auto px-4">
          <div className="flex items-center justify-center space-x-2 text-sm text-gray-300">
            <Info className="h-4 w-4 text-gray-400" />
            <span>데이터 출처:</span>
            <a 
              href="https://www.data.go.kr/data/15100065/standard.do"
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary-400 hover:text-primary-300 underline"
            >
              공공데이터포털 - 전국통합식품영양성분정보(원재료성식품)표준데이터
            </a>
            <span className="text-gray-500">|</span>
            <span className="text-xs text-gray-400">Mock 데이터 사용 중</span>
          </div>
        </div>
      </footer>
    </div>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <NutritionCalculator />
    </QueryClientProvider>
  );
}

export default App;