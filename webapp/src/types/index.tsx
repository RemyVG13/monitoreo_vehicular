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

export interface Alarm extends BaseContentElement{
  date: string;
  hour: string;
  reason: string;
  teacher_name: string;
  car_name:string;
  thingspeak_id: number;
}

export interface HistoryData{
  coords_list: [number,number][];
  dates_list: string[];
  teacher_name_list: string[]
}
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
  key: keyof T;
  label: string;
}

