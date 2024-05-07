import { apiclient, configHeader } from './authService';
import { Teacher } from '@/types';
import { FormDataObject } from '@/types';

export const fetchAllTeachers = async (token: string, type: string, search: string) => {
  try {
    const response = await apiclient.get(`teachers/?search=${search}`, {
      headers: configHeader(token, type),
    });
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error("Error fetching car data:", error);
    throw error;
  }
}


export const fetchTeacher = async (token: string, type: string, teacher_id: string) => {
  try {
    const response = await apiclient.get(`teachers/${teacher_id}`, {
      headers: configHeader(token, type),
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching teacher:", error);
    throw error;
  }
}


export const deleteTeacher = async (token: string, type: string, teacher_id: string | null) => {
  try {
    console.log("deleteTeacher");
    console.log(token);
    const response = await apiclient.delete(`teachers/${teacher_id}`, {
      headers: configHeader(token, type),
    });
    return response.data;
  } catch (error) {
    console.error("Error deleting teacher:", error);
    throw error;
  }
}


export const updateTeacher = async (token: string, type: string, teacher_id: string | null, formData: FormDataObject) => {
  try {
    console.log("updateTeacher");
    console.log(token);
    const response = await apiclient.put(`teachers/${teacher_id}`, formData, {
      headers: configHeader(token, type),
    });
    console.log("Services/teachers => updateTeacher: " + response.data);
    return response.statusText;
  } catch (error: any) {
    console.log("Error Services/teachers => updateTeacher: " + error.response.data.detail)
    console.log(error);
    return error.response.data.detail
  }
}

export const createTeacher = async (token: string, type: string, formData: FormDataObject) => {
  try {
    console.log("createTeacher");
    console.log(token);
    const response = await apiclient.post(`teachers/`, formData, {
      headers: configHeader(token, type),
    });
    console.log("Services/teachers => createTeacher: " + response.data);
    return response.statusText;
  } catch (error: any) {
    console.log("Error Services/teachers => createTeacher: " + error.response.data.detail)
    console.log(error);
    return error.response.data.detail
  }
}
