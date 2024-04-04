// src/utils/authUtils.tsx
"use client";
export const getAuthDetails = () => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('token'); // Asume que guardaste el token aquí al iniciar sesión
      const type = 'Bearer'; // Tipo de autenticación, generalmente es Bearer para tokens JWT
      return { token, type };
    }
    // Devuelve valores por defecto o nulos si se ejecuta en el servidor
    return { token: null, type: null };
  };
  
  