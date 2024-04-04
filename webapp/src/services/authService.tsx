import { NextApiRequest, NextApiResponse } from 'next';
import axios, { AxiosError,AxiosRequestConfig } from "axios"
import Error from 'next/error';

export const apiclient = axios.create({
    //baseURL: `${process.env.NEXT_PUBLIC_SERVER_API_URL}`, 
    baseURL: `http://localhost:8000`, 
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

        // Asume éxito y extrae el token u otra info relevante de la respuesta
        return { success: true, message: 'Login successful', data: response.data };
    } catch (error) {
        console.log("Authentication => authenticate error: " + error);
        // Ajusta la respuesta de error según la estructura de tus errores
        return { success: false, message: 'Login failed', data: null };
    }    
}
