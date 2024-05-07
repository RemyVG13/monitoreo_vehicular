'use client';
import React from 'react'
import { useState } from 'react';
import { useEffect } from 'react';
import { useRouter } from "next/navigation";
import { JWT } from '@/types';


export default function ReportsPage () {
  const router = useRouter();
  const [JWT, setToken] = useState<JWT>({ token:'', type:''});

  
  return (
    <div>
        <div>REPORTS</div>    
    </div>
  )
}
 


