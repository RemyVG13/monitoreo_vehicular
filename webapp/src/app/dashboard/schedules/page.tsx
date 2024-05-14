'use client';
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { fetchDetailSchedules, deleteSchedule } from '@/services/scheduleService';
import { getAuthDetails } from '@/utils/authUtils';
import { Schedule, Column } from '@/types';
import Table from '@/components/Table';
import SearchBar from '@/components/SearchTable';
import AddButton from '@/components/addButton';

export default function SchedulesPage() {
  const [schedules, setSchedules] = useState<Schedule[]>([]);
  const { token, type } = getAuthDetails();
  const validToken = token ?? '';
  const validType = type ?? '';
  const router = useRouter();

  useEffect(() => {
    handleSearch("");
  }, []); // Loads the initial schedule data

  const handleSearch = async (searchTerm: string) => {
    try {
      const fetchedSchedules = await fetchDetailSchedules(validToken, validType, searchTerm);
      setSchedules(fetchedSchedules);
    } catch (error) {
      console.error('Error fetching schedules:', error);
    }
  };

  const handleDelete = async (deleteToken: string, deleteType: string,scheduleId: string | null) => {
    
    try {
      const response = await deleteSchedule(deleteToken, deleteType, scheduleId);
      console.log("SCHEDULE PAGE DELETE RESPONSE")
      console.log(response)
      handleSearch(""); // Refresh the list after deleting

    } catch (error) {
      console.error('Error deleting schedule:', error);
    }
  };
  /**
   
   */
  const handleAdd = () => {
    router.push('/dashboard/schedules/create');
  };

  const columns: Column<Schedule>[] = [
    { key: 'teacher_name', label: 'INSTRUCTOR' },
    { key: 'car_name', label: 'AUTO' },
    { key: 'day', label: 'DÍA' },
    { key: 'hour_hhmm', label: 'HORA' },
  ];

  return (
    <div style={{ margin: '80px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px', alignItems: 'center' }}>
        <SearchBar onSearch={handleSearch} />
        <AddButton onClick={handleAdd} />
      </div>
      <Table<Schedule> columns={columns} data={schedules} modalMessage={"Are you sure you want to delete this schedule?"} confirmDeleteModal={handleDelete} tableToken={validToken} tableType={validType} />
    </div>
  );
}
