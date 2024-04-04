import { useEffect,useState } from 'react';

export interface CarData {
    date: string;
    fuel: string;
    latitude: string;
    longitude: string;
    speed: string;
  }
  
const [data, setData] = useState<CarData[]>([]);
  