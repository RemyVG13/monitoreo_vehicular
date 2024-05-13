'use client';
import React from 'react';
import dynamic from 'next/dynamic';
import { useRouter } from 'next/navigation';
import { getAuthDetails } from '@/utils/authUtils';
import CarMapDetail from '@/components/CarMapDetail';
import { useState,useEffect } from 'react';

const MapComponent = dynamic(() => import('@/components/MapComponent'), {
  ssr: false  // No renderizar del lado del servidor
});

export default function MapPage() {
  const [coordsFromMapDetail, setcoordsFromMapDetail] = useState<[number, number][]>([[0, 0]]);
  const [teacherFromMapDetail, setTeacherFromMapDetail] = useState<string[]>([""]);
  const [dateFromMapDetail, setDateFromMapDetail] = useState<string[]>([""]);
  const handleReceivedCoords = (msg: [number, number][], msg2: string[], msg3: string[]) => {
    setcoordsFromMapDetail(msg);
    setTeacherFromMapDetail(msg2);
    setDateFromMapDetail(msg3);
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
            <MapComponent markers={coordsFromMapDetail} names={teacherFromMapDetail} dates={dateFromMapDetail}/>
          </div>
        </div>
      </div>
      
    </div>
  );
}

