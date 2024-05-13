'use client';
import React from 'react'
import { useState } from 'react';
import { useEffect } from 'react';
import { useRouter } from "next/navigation";
import { JWT } from '@/types';
import { CarLineChart } from '@/components/LineChartComponent';

export default function ReportsPage () {
  const router = useRouter();
  const [JWT, setToken] = useState<JWT>({ token:'', type:''});

  
  return (
    <div>
        <div>REPORTS</div>
        <CarLineChart dataSets={[
          {
            name: 'Toyota Corolla',
            data: [{x: '2021-01-01', y: 12}, {x: '2021-02-01', y: 19},{x: '2021-01-01', y: 15}, {x: '2021-02-01', y: 23}]
          },
          {
            name: 'Honda Civic',
            data: [{x: '2021-01-01', y: 15}, {x: '2021-02-01', y: 23},{x: '2021-01-01', y: 15}, {x: '2021-02-01', y: 23}]
          }
        ]}/>    
    </div>
  )
}
 


