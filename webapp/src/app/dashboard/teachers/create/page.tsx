'use client';
import React from 'react'
import { useRouter } from "next/navigation";
import CreateTeacher from '@/components/CreateTeacher';
import { getAuthDetails } from '@/utils/authUtils';

export default function CreateTeacherPage () {
  const router = useRouter();
  const { token, type } = getAuthDetails();
  const validToken = token ?? '';
  const validType = type ?? '';

  const backToTeachers = () => {
    router.push('/dashboard/teachers');
  };

  return (
    <div style={{ margin: '80px', paddingLeft:"40px",paddingRight:"40px", paddingBottom:"40px",paddingTop:"5px"}} className='bg-white'>
      <CreateTeacher
        backToTeachers={backToTeachers}
        createToken={validToken} 
        createType={validType}  
      />
    </div>
  );
}
 


