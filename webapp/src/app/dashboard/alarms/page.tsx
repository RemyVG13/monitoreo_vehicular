'use client';
import React from 'react'
import { useState } from 'react';
import { useEffect } from 'react';
import { useRouter } from "next/navigation";
import { JWT } from '@/types';


export default function AlarmsPage () {
  const router = useRouter();
  const [JWT, setToken] = useState<JWT>({ token:'', type:''});

  
  return (
    <div>
        <div>ALARMS</div>    
    </div>
  )
}
 


