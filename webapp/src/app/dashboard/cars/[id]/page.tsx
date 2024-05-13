'use client';
import EditCar from '@/components/EditCar';
import { useRouter } from 'next/navigation';
import { getAuthDetails } from '@/utils/authUtils';

export default function CarPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const { token, type } = getAuthDetails();
  const validToken = token ?? '';
  const validType = type ?? '';

  const backToCars = () => {
    router.push('/dashboard/cars');
  };

  return (
    <div style={{ margin: '80px', paddingLeft:"40px",paddingRight:"40px", paddingBottom:"40px",paddingTop:"5px"}} className='bg-white'>
      <EditCar
        car_id={params.id}
        backToCars={backToCars}
        editToken={validToken}  
        editType={validType} 
      />
    </div>
  );
}
