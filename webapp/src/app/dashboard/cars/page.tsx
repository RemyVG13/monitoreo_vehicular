'use client';
import React, { useState, useEffect } from 'react';
import { fetchAllCars, deleteCar } from '@/services/carService';
import { getAuthDetails } from '@/utils/authUtils';
import { Car, Column, BaseContentElement } from '@/types';
import Table from '@/components/Table';
import SearchBar from '@/components/SearchTable';
import { useRouter } from "next/navigation";
import AddButton from '@/components/addButton';

export default function CarsPage() {
  const [cars, setCars] = useState<Car[]>([]);
  const { token, type } = getAuthDetails();
  const validToken = token ?? '';
  const validType = type ?? '';

  const router = useRouter();
  useEffect(() => {
    handleSearch("");
  }, []); // Ejecuta solo una vez al montar el componente

  const handleSearch = async (searchTerm: string) => {
    try {
      const fetchedData = await fetchAllCars(validToken, validType, searchTerm);
      setCars(fetchedData);
    } catch (error) {
      console.error(error);
    }
  };

  const handleDelete = async (deleteToken: string, deleteType: string,searchTerm: string | null) => {
    try {
      const response = await deleteCar(deleteToken, deleteType, searchTerm);
      handleSearch("");
    } catch (error) {
      console.error(error);
    }
  };

  const handleAdd = () => {
    router.push('/dashboard/cars/create');
  };

  const columns: Column<Car>[] = [
    { key: 'name', label: 'NOMBRE' },
    { key: 'plate', label: 'MATRÍCULA' },
    { key: 'make', label: 'MARCA' },
    { key: 'model', label: 'MODELO' },
    { key: 'year', label: 'AÑO' }
  ];

  return (
    <div style={{ margin: '80px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px', alignItems: 'center' }}>
        <SearchBar onSearch={handleSearch} />
        <AddButton onClick={handleAdd} />
      </div>
      <Table<Car>
        columns={columns}
        data={cars}
        modalMessage={"¿Estás seguro que deseas eliminar este automóvil?"}
        confirmDeleteModal={handleDelete}
        tableToken={validToken}
        tableType={validType}
      />
    </div>
  );
};
