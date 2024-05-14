'use client';
import React from 'react'
import { useState } from 'react';
import { useEffect } from 'react';
import { useRouter } from "next/navigation";
import { JWT } from '@/types';
import { CarLineChart } from '@/components/LineChartComponent';
import ReportComponent from '@/components/ReportComponent';
import { getAuthDetails } from '@/utils/authUtils';
import { Report } from '@/types';

export default function ReportsPage () {
  const router = useRouter();
  const [JWT, setToken] = useState<JWT>({ token:'', type:''});
  const { token, type } = getAuthDetails();
  const validToken = token ?? '';
  const validType = type ?? '';
  const [reports, setReports] = useState<Report[]>([]);
  const handleReceivedReports = (rep: Report[]) => {
    setReports(rep);
  };


  useEffect(() => {
    // Simulación de datos recibidos del servidor
    const fetchedReports: Report[] = [
      {
        car_name: "Prueba Suzuki",
        report_type: "Distancia",
        report: [
          ["10 de Mayo, 2024. A las 06:32 AM", 0],
          ["11 de Mayo, 2024. A las 06:32 AM", 0],
          ["12 de Mayo, 2024. A las 06:32 AM", 0],
          ["13 de Mayo, 2024. A las 06:32 AM", 1.34],
        ],
      },
      {
        car_name: "CALDINA 2005ZTE",
        report_type: "Distancia",
        report: [
          ["10 de Mayo, 2024. A las 06:32 AM", 0],
          ["11 de Mayo, 2024. A las 06:32 AM", 20.09],
          ["12 de Mayo, 2024. A las 06:32 AM", 48.96],
          ["13 de Mayo, 2024. A las 06:32 AM", 78.76],
        ],
      },
    ];

    setReports(fetchedReports);
  }, []);



  return (
    <div style={{ margin: '30px' }}>
      <div className='container-fluid'>
        <div className='row'>
          <div className='col-sm-12 col-lg-4 bg-white shadow rounded'>
              {/* <CarMapDetail carToken={validToken} carType={validType} setcoords={handleReceivedCoords}/> */}
              <ReportComponent carToken={validToken} carType={validType} setReports = {handleReceivedReports}/>
          </div>
          <div className='col-lg-1 '>
          </div>
          <div className='col-sm-12 col-lg-7 bg-white shadow  p-0 rounded '>
            <div className='m-4'>
              <CarLineChart  reports={reports}/>
            </div>
            
          </div>
        </div>
      </div>
    </div>  
  )
}
 


