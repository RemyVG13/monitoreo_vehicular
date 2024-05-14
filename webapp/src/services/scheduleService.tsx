import { apiclient, configHeader } from './authService';
import { Schedule } from '@/types';
import { FormDataObject } from '@/types';

export const fetchAllSchedules = async (token: string, type: string, search: string) => {
  try {
    const response = await apiclient.get(`schedules/?search=${search}`, {
      headers: configHeader(token, type),
    });
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error("Error fetching schedules:", error);
    throw error;
  }
}

export const fetchDetailSchedules = async (token: string, type: string, search: string) => {
  try {
    const response = await apiclient.get(`schedules/detail/?search=${search}`, {
      headers: configHeader(token, type),
    });
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error("Error fetching detail schedules:", error);
    throw error;
  }
}

export const fetchSchedule = async (token: string, type: string, schedule_id: string) => {
  try {
    const response = await apiclient.get(`schedules/${schedule_id}`, {
      headers: configHeader(token, type),
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching schedule:", error);
    throw error;
  }
}


export const deleteSchedule = async (token: string, type: string, schedule_id: string | null) => {
  try {
    console.log("schedule token",token)
    console.log("schedule type",type)
    console.log("schedule id",schedule_id)
    const response = await apiclient.delete(`schedules/${schedule_id}`, {
      headers: configHeader(token, type),
    });
    return response.data;
  } catch (error) {
    console.error("Error deleting schedule:", error);
    throw error;
  }
}


export const updateSchedule = async (token: string, type: string, schedule_id: string | null, formData: FormDataObject) => {
  try {
    console.log("updateSchedule");
    console.log(token);
    const response = await apiclient.put(`schedules/${schedule_id}`, formData, {
      headers: configHeader(token, type),
    });
    console.log("Services/schedules => updateSchedule: " + response.data);
    return response.statusText;
  } catch (error: any) {
    console.log("Error Services/schedules => updateSchedule: " + error.response.data.detail)
    console.log(error);
    return error.response.data.detail
  }
}

export const createSchedule = async (token: string, type: string, formData: FormDataObject) => {
  try {
    console.log("createSchedule");
    console.log(token);
    const response = await apiclient.post(`schedules/`, formData, {
      headers: configHeader(token, type),
    });
    console.log("Services/schedules => createSchedule: " + response.data);
    return response.statusText;
  } catch (error: any) {
    console.log("Error Services/schedule => createSchedule: " + error.response.data.detail)
    console.log(error);
    return error.response.data.detail
  }
}
