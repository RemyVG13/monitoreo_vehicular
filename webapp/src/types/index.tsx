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
  /*
  class UpdateUser(UpdateBaseContent):
    first_name: Union[str, None] = None
    father_last_name: Union[str, None] = None
    mother_last_name: Union[str, None] = None
    id_number: Union[int, None] = None
    id_zone: Union[str, None] = None #Zones Class
    birthday_date_inseconds: Union[int, None] = None
    rol: Union[str, None] = None
  */
export interface JWT {
  token: string;
  type: string;
}

export interface Column<T> {
  key: keyof T;  // 'key' es una clave del tipo genérico T
  label: string; // 'label' es el texto que se mostrará en la cabecera de la tabla
}

