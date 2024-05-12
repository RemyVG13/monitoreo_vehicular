import { useEffect,useState } from 'react';
export interface BaseContentElement{
  id: string;
  disabled?: boolean;
  creation_date_inseconds?: number;
  creator_id?: string;
  history_element?: boolean;
  deleted?: boolean;
}
export interface CarData {
    date: string;
    fuel: string;
    latitude: string;
    longitude: string;
    speed: string;
  }

export type FormDataObject = Record<string, string | number>;

export interface Teacher extends BaseContentElement{
  first_name: string;
  father_last_name: string;
  mother_last_name: string;
  id_number: number;
  birthday_date_inseconds: number;
  id_zone: string;
}

export interface Car extends BaseContentElement{
  name: string;
  plate: string;
  make: string;
  model: string;
  year: number;
  thingspeak_id: number;
}

export interface MapCarDetail extends BaseContentElement{
  name: string;
  plate: string;
  make: string;
  model: string;
  year: number;
  thingspeak_id: number;
  full_name: string;
  teacher_name: string;
  longitude:number;
  latitude: number;
  fuel:number;
  speed: number;
  state: string;
  zone: string;
  is_working: string;
  teacher_id: string;
  last_time:string;
}

/*{
    "id": "660b2e4996c36ca01404f6e0",
    "name": "CALDINA 2005ZTE",
    "plate": "2005 ZTE",
    "make": "TOYOTA",
    "model": "CALDINA",
    "year": 1999,
    "thingspeak_id": 2425622,
    "full_name": "TOYOTA CALDINA 1999 2005 ZTE",
    "teacher_name": "Paola Vicario",
    "longitude": -66.31427,
    "latitude": -17.396368,
    "fuel": 42.6,
    "speed": 50,
    "state": "Inactivo",
    "zone": "Fuera de zona",
    "teacher_id": "64c9e0f425576f886d74705f"
}*/
export interface Schedule extends BaseContentElement{
  teacher_id: string;
  car_id: string;
  teacher_name: string;
  car_name: string;
  day: string;
  hour: number;
  hour_hhmm: string;
}


export interface JWT {
  token: string;
  type: string;
}

export interface Column<T> {
  key: keyof T;  // 'key' es una clave del tipo genérico T
  label: string; // 'label' es el texto que se mostrará en la cabecera de la tabla
}

