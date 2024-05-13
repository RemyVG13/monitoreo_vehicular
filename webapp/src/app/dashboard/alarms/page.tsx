'use client';
import React, { useState, useEffect } from 'react';
import { fetchAllAlarms } from '@/services/alarmService';
import { getAuthDetails } from '@/utils/authUtils';
import { Alarm, Column } from '@/types';
import Table from '@/components/Table';
import SearchBar from '@/components/SearchTable';
import { useRouter } from "next/navigation";

export default function AlarmsPage() {
  const [alarms, setAlarms] = useState<Alarm[]>([]);
  const { token, type } = getAuthDetails();
  const validToken = token ?? '';
  const validType = type ?? '';
  const router = useRouter();

  useEffect(() => {
    handleSearch("");
  }, []); // Ejecuta solo una vez al montar el componente

  const handleSearch = async (searchTerm: string) => {
    try {
      const fetchedData = await fetchAllAlarms(validToken, validType, searchTerm);
      setAlarms(fetchedData);
    } catch (error) {
      console.error("Error fetching alarms:", error);
    }
  };

  const columns: Column<Alarm>[] = [
    { key: 'date', label: 'Fecha' },
    { key: 'hour', label: 'Hora' },
    { key: 'reason', label: 'Motivo' },
    { key: 'teacher_name', label: 'Instructor' },
    { key: 'car_name', label: 'Auto' },
  ];

  return (
    <div style={{ margin: '100px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px', alignItems: 'center' }}>
        <SearchBar onSearch={handleSearch} />
      </div>
      <Table<Alarm> columns={columns} data={alarms} modalMessage="¿Estás seguro que deseas eliminar esta alarma?" confirmDeleteModal={() => {}} tableToken={"-"} tableType={"-"} />
    </div>
  );
};
