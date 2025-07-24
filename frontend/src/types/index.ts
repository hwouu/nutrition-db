// API Response Types
export interface NutritionInfo {
  food_code: string;
  food_name: string;
  nutrition_base_amount?: string;
  energy?: number;
  water?: number;
  protein?: number;
  fat?: number;
  ash?: number;
  carbohydrate?: number;
  sugar?: number;
  dietary_fiber?: number;
  calcium?: number;
  iron?: number;
  phosphorus?: number;
  potassium?: number;
  sodium?: number;
  vitamin_a?: number;
  retinol?: number;
  beta_carotene?: number;
  thiamine?: number;
  riboflavin?: number;
  niacin?: number;
  vitamin_c?: number;
  vitamin_d?: number;
  cholesterol?: number;
  saturated_fat?: number;
  trans_fat?: number;
  refuse_rate?: number;
  source_code?: string;
  source_name?: string;
}

export interface FoodComposition {
  ingredient_name: string;
  percentage: number;
  unit: string;
  preparation?: string;
}

export interface ComplexFood {
  food_name: string;
  compositions: FoodComposition[];
  total_weight: number;
  description?: string;
}

export interface CalculatedNutrition {
  food_name: string;
  weight_grams: number;
  energy?: number;
  protein?: number;
  fat?: number;
  carbohydrate?: number;
  sugar?: number;
  dietary_fiber?: number;
  calcium?: number;
  iron?: number;
  sodium?: number;
  potassium?: number;
  vitamin_a?: number;
  vitamin_c?: number;
  composition_details?: CompositionDetail[];
}

export interface CompositionDetail {
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
}

export interface NutritionResponse {
  success: boolean;
  message: string;
  data?: CalculatedNutrition;
}

export interface NutritionCalculationRequest {
  food_name: string;
  weight_grams: number;
}

// UI State Types
export interface FoodSelection {
  id: string;
  food_name: string;
  weight_grams: number;
  nutrition?: CalculatedNutrition;
  status: 'idle' | 'calculating' | 'completed' | 'error';
}

export interface DashboardStats {
  totalCalories: number;
  totalWeight: number;
  totalFoods: number;
  caloriesChange: number;
  weightChange: number;
}

export interface PopularFood {
  name: string;
  count: number;
  averageCalories: number;
  percentage: number;
}

// Chart Data Types
export interface ChartData {
  name: string;
  value: number;
  color?: string;
}

export interface NutritionChartData {
  name: string;
  calories: number;
  protein: number;
  fat: number;
  carbs: number;
}

// Navigation Types
export interface NavigationItem {
  id: string;
  name: string;
  icon: React.ComponentType<any>;
  href: string;
  current: boolean;
}