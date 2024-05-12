'use client';
import React from 'react';
import dynamic from 'next/dynamic';
import { useRouter } from 'next/navigation';
import { getAuthDetails } from '@/utils/authUtils';
import CarMapDetail from '@/components/CarMapDetail';
import { useState,useEffect } from 'react';
// Importa dinámicamente el MapComponent, asegurando que no se intente cargar en el servidor
const MapComponent = dynamic(() => import('@/components/MapComponent'), {
  ssr: false  // No renderizar del lado del servidor
});

export default function MapHistoryPage() {
  const [coordsFromMapDetail, setcoordsFromMapDetail] = useState<[number, number][]>([[-17.41047981158394, -66.29267798176957]]);
  const handleReceivedCoords = (msg: [number, number][]) => {
    setcoordsFromMapDetail(msg);
  };
  const { token, type } = getAuthDetails();
  const validToken = token ?? '';
  const validType = type ?? '';
  const router = useRouter();

  useEffect(() => {
    console.log("coordsFromMapDetail",coordsFromMapDetail)
  }, [coordsFromMapDetail]);

  return (
    <div style={{ margin: '30px' }}>
      <div className='container-fluid'>
        <div className='row'>
          <div className='col-lg-4 bg-white shadow rounded'>
            <CarMapDetail carToken={validToken} carType={validType} setcoords={handleReceivedCoords}/>
          </div>
          <div className='col-lg-8 rounded'>
            <MapComponent markers={coordsFromMapDetail}/>
          </div>
        </div>
      </div>
      
    </div>
  );
}

