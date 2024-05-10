'use client';
import React from 'react';
import CreateSchedule from '@/components/CreateSchedule';
import { useRouter } from 'next/navigation';
import { getAuthDetails } from '@/utils/authUtils';

export default function CreateSchedulePage() {
    const router = useRouter();
    const { token, type } = getAuthDetails();
    const validToken = token ?? '';
    const validType = type ?? '';

    // Función para manejar el retorno a la lista de horarios
    const backToSchedules = () => {
        router.push('/dashboard/schedules');
    };

    return (
        <div style={{ margin: '80px', paddingLeft:"40px",paddingRight:"40px", paddingBottom:"40px",paddingTop:"5px"}} className='bg-white'>
            <CreateSchedule
                backToSchedules={backToSchedules}
                createToken={validToken}
                createType={validType}
            />
        </div>
    );
}
