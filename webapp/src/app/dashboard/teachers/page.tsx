'use client';
import React, { useState } from 'react';
import { fetchAllTeachers,deleteTeacher } from '@/services/teacherService';
import { getAuthDetails } from '@/utils/authUtils';
import { Teacher, Column, BaseContentElement } from '@/types';
import Table from '@/components/Table';
import SearchBar from '@/components/SearchTable';
import { useEffect } from 'react';
import { useRouter } from "next/navigation";
import AddButton from '@/components/addButton';


export default function TeachersPage() {
  const [teachers, setTeachers] = useState<Teacher[]>([]);
  const { token, type } = getAuthDetails();
  const validToken = token ?? '';
  const validType = type ?? '';


  const router = useRouter();
  useEffect(() => {
    //console.log(token);
    handleSearch("");
  }, []); // Ejecuta solo una vez al montar el componente


  const handleSearch = async (searchTerm: string) => {
    try {
    const fetchedData = await fetchAllTeachers(validToken, validType, searchTerm);
    //console.log(fetchedData);
    setTeachers(fetchedData);
    } catch (error) {
    console.error(error);
    }
  };

  const handleDelete = async (deleteToken: string, deleteType: string,searchTerm: string | null) => {
    
    try {
      const reponse = await deleteTeacher(deleteToken, deleteType, searchTerm);
      //console.log(reponse);
      handleSearch("");
      //router.push('/dashboard/teachers');
    } catch (error) {
      console.error(error);
    }
  };
  const handleAdd = () => {
    // Define la acción de añadir (ej., abrir un modal o redirigir a otra página)
    router.push('/dashboard/teachers/create');
  };

  const columns: Column<Teacher>[] = [
    { key: 'first_name', label: 'NOMBRE' },
    { key: 'father_last_name', label: 'APELLIDO PATERNO' },
    { key: 'mother_last_name', label: 'APELLIDO MATERNO' },
    { key: 'id_number', label: 'CARNET' },
    { key: 'id_zone', label: 'ZONA' },
  ];
  

  return (
    <div style={{ margin: '80px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px', alignItems: 'center' }}>
        <SearchBar onSearch={handleSearch} />
        <AddButton onClick={handleAdd} />
      </div>
        <Table<Teacher> columns={columns} data={teachers} modalMessage={"¿Estás seguro que deseas eliminar al maestro ?"} confirmDeleteModal={handleDelete} tableToken={validToken} tableType={validType}/>
    </div>
  );
};


