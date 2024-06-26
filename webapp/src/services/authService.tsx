import { NextApiRequest, NextApiResponse } from 'next';
import axios, { AxiosError,AxiosRequestConfig } from "axios"
import Error from 'next/error';

export const apiclient = axios.create({
    baseURL: `${process.env.NEXT_PUBLIC_SERVER_API_URL}`, 
    proxy: false  
  })

   
export const configHeader = (token: string,type: string) => {
    return {
        "Content-Type": "application/json",
        "Authorization": `${type} ${token}`,
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT",
      }
}

export async function loginUser(username: string, password: string) {
    let bodyFormData = new FormData();
    bodyFormData.append('username', username);
    bodyFormData.append('password', password);
    try {
        console.log("authenticate Function starting");
        const response = await apiclient.post("login", bodyFormData, {
            headers: {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
                "Access-Control-Allow-Headers": "*",
            }    
        });
        return { success: true, message: 'Login successful', data: response.data };
    } catch (error) {
        console.log("Authentication => authenticate error: " + error);
        return { success: false, message: 'Login failed', data: null };
    }    
}
