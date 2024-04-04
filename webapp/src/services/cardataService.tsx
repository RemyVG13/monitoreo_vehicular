import { apiclient, configHeader } from './authService';

export const fetchCarData = async (token: string, type: string, vehicle_id: number, amount: number) => {
  try {
    const response = await apiclient.get(`cardatas/?vehicle_id=${vehicle_id}&amount=${amount}`, {
      headers: configHeader(token, type),
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching car data:", error);
    throw error;
  }
}
