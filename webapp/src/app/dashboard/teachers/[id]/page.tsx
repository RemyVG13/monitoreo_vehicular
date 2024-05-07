'use client';
import EditTeacher from '@/components/EditTeacher';
import { useRouter } from 'next/navigation';
import { getAuthDetails } from '@/utils/authUtils';


export default function TeacherPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const { token, type } = getAuthDetails();
  const validToken = token ?? '';
  const validType = type ?? '';

  // Función para volver a la lista de maestros
  const backToTeachers = () => {
    router.push('/dashboard/teachers');
  };

  return (
    <div style={{ margin: '80px', paddingLeft:"40px",paddingRight:"40px", paddingBottom:"40px",paddingTop:"5px"}} className='bg-white'>
      <EditTeacher
        teacher_id={params.id}
        backToTeachers={backToTeachers}
        editToken={validToken}  // Reemplaza con el token real
        editType={validType}  // Reemplaza con el tipo real
      />
    </div>
  );
}




