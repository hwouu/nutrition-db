import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { nutritionApi } from '../services/api';
import type { NutritionCalculationRequest } from '../types';

// Query keys
const QUERY_KEYS = {
  foods: ['foods'] as const,
  foodComposition: (name: string) => ['foods', name] as const,
  nutrition: (request: NutritionCalculationRequest) => ['nutrition', request] as const,
  health: ['health'] as const,
};

// Hook for fetching available foods
export const useFoods = () => {
  return useQuery({
    queryKey: QUERY_KEYS.foods,
    queryFn: nutritionApi.getFoodList,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

// Hook for fetching food composition
export const useFoodComposition = (foodName: string, enabled: boolean = true) => {
  return useQuery({
    queryKey: QUERY_KEYS.foodComposition(foodName),
    queryFn: () => nutritionApi.getFoodComposition(foodName),
    enabled: enabled && !!foodName,
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
};

// Hook for calculating nutrition
export const useCalculateNutrition = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: nutritionApi.calculateNutrition,
    onSuccess: (data, variables) => {
      // Cache the result
      queryClient.setQueryData(
        QUERY_KEYS.nutrition(variables),
        data
      );
    },
  });
};

// Hook for health check
export const useHealthCheck = () => {
  return useQuery({
    queryKey: QUERY_KEYS.health,
    queryFn: nutritionApi.healthCheck,
    refetchInterval: 30 * 1000, // 30 seconds
    retry: 1,
  });
};