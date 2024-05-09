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
/**
  name: str
  plate: str
  make: str
  model: str
  year: int
  thingspeak_id: int
 */
export interface JWT {
  token: string;
  type: string;
}

export interface Column<T> {
  key: keyof T;  // 'key' es una clave del tipo genérico T
  label: string; // 'label' es el texto que se mostrará en la cabecera de la tabla
}

