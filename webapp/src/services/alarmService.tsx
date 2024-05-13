import { apiclient, configHeader } from './authService';
import { FormDataObject } from '@/types';

export const fetchAllAlarms = async (token: string, type: string, search: string) => {
  try {
    const response = await apiclient.get(`alarms/?search=${search}`, {
      headers: configHeader(token, type),
    });
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error("Error fetching alarms:", error);
    throw error;
  }
}

export const fetchAlarm = async (token: string, type: string, alarm_id: string) => {
  try {
    const response = await apiclient.get(`alarms/${alarm_id}`, {
      headers: configHeader(token, type),
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching alarm:", error);
    throw error;
  }
}

