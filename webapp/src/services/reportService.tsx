import { apiclient, configHeader } from './authService';
import { FormDataObject } from '@/types';


export const fetchReport = async (token: string, type: string, car_id: string, start_date:string, end_date:string, period:string, report_type:string) => {
  try {
    const response = await apiclient.get(`reports/?car_id=${car_id}&start_date=${start_date}&end_date=${end_date}&period=${period}&report_type=${report_type}`, {
      headers: configHeader(token, type),
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching report:", error);
    throw error;
  }
}

/**
 {
  "car_name": "CALDINA 2005ZTE",
  "report_type": "Distancia",
  "report": [
    [
      "01 de Mayo, 2024. A las 05:19 PM",
      0
    ],
    [
      "02 de Mayo, 2024. A las 05:19 PM",
      0
    ],
    [
      "03 de Mayo, 2024. A las 05:19 PM",
      0
    ],
    [
      "04 de Mayo, 2024. A las 05:19 PM",
      0
    ],
    [
      "05 de Mayo, 2024. A las 05:19 PM",
      0
    ],
    [
      "06 de Mayo, 2024. A las 05:19 PM",
      0
    ],
    [
      "07 de Mayo, 2024. A las 05:19 PM",
      0
    ],
    [
      "08 de Mayo, 2024. A las 05:19 PM",
      0
    ],
    [
      "09 de Mayo, 2024. A las 05:19 PM",
      0
    ],
    [
      "10 de Mayo, 2024. A las 05:19 PM",
      0
    ],
    [
      "11 de Mayo, 2024. A las 05:19 PM",
      34.76
    ],
    [
      "12 de Mayo, 2024. A las 05:19 PM",
      67.15
    ]
  ]
}
 */