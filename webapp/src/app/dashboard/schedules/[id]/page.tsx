'use client';
import React from 'react';
import EditSchedule from '@/components/EditSchedule';
import { useRouter } from 'next/navigation';
import { getAuthDetails } from '@/utils/authUtils';

export default function ScheduleDetailPage({ params }: { params: { id: string } }) {
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
        <EditSchedule
          schedule_id={params.id}
          backToSchedules={backToSchedules}
          editToken={validToken}
          editType={validType}
        />
      </div>
    );
}
