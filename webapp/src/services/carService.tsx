import { apiclient, configHeader } from './authService';
import { Car } from '@/types';
import { FormDataObject } from '@/types';

export const fetchAllCars = async (token: string, type: string, search: string) => {
  try {
    const response = await apiclient.get(`cars/?search=${search}`, {
      headers: configHeader(token, type),
    });
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error("Error fetching cars:", error);
    throw error;
  }
}


export const fetchCar = async (token: string, type: string, car_id: string) => {
  try {
    const response = await apiclient.get(`cars/${car_id}`, {
      headers: configHeader(token, type),
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching car:", error);
    throw error;
  }
}

export const fetchMapCar = async (token: string, type: string, car_id: string) => {
  try {
    const response = await apiclient.get(`cars/mapdetail/${car_id}`, {
      headers: configHeader(token, type),
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching map car:", error);
    throw error;
  }
}

export const fetchHistoryCar = async (token: string, type: string, car_id: string,startDate: string,endDate:string) => {
  try {
    const response = await apiclient.get(`cars/history/${car_id}/?start_date=${startDate}&end_date=${endDate}`, {
      headers: configHeader(token, type),
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching history car:", error);
    throw error;
  }
}

export const deleteCar = async (token: string, type: string, car_id: string | null) => {
  try {
    const response = await apiclient.delete(`cars/${car_id}`, {
      headers: configHeader(token, type),
    });
    return response.data;
  } catch (error) {
    console.error("Error deleting car:", error);
    throw error;
  }
}


export const updateCar = async (token: string, type: string, car_id: string | null, formData: FormDataObject) => {
  try {
    console.log("updateCar");
    console.log(token);
    const response = await apiclient.put(`cars/${car_id}`, formData, {
      headers: configHeader(token, type),
    });
    console.log("Services/cars => updateCar: " + response.data);
    return response.statusText;
  } catch (error: any) {
    console.log("Error Services/cars => updateCar: " + error.response.data.detail)
    console.log(error);
    return error.response.data.detail
  }
}

export const createCar = async (token: string, type: string, formData: FormDataObject) => {
  try {
    console.log("createCar");
    console.log(token);
    const response = await apiclient.post(`cars/`, formData, {
      headers: configHeader(token, type),
    });
    console.log("Services/cars => createCar: " + response.data);
    return response.statusText;
  } catch (error: any) {
    console.log("Error Services/car => createCar: " + error.response.data.detail)
    console.log(error);
    return error.response.data.detail
  }
}
