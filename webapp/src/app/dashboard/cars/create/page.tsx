'use client';
import React from 'react';
import { useRouter } from "next/navigation";
import CreateCar from '@/components/CreateCar';
import { getAuthDetails } from '@/utils/authUtils';

export default function CreateCarPage() {
  const router = useRouter();
  const { token, type } = getAuthDetails();
  const validToken = token ?? '';
  const validType = type ?? '';

  // Función para volver a la lista de automóviles
  const backToCars = () => {
    router.push('/dashboard/cars');
  };

  return (
    <div style={{ margin: '80px', paddingLeft: "40px", paddingRight: "40px", paddingBottom: "40px", paddingTop: "5px" }} className='bg-white'>
      <CreateCar
        backToCars={backToCars}
        createToken={validToken}
        createType={validType}
      />
    </div>
  );
}
