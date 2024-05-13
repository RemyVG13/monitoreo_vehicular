"use client";
export const getAuthDetails = () => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('token'); 
      const type = 'Bearer'; 
      return { token, type };
    }
    return { token: null, type: null };
  };
  
  