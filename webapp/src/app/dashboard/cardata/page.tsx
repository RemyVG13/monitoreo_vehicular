'use client';
import React, { useState } from 'react';
import { fetchCarData } from '@/services/cardataService';
import { getAuthDetails } from '@/utils/authUtils';
import { CarData } from '@/types';
import { JWT } from '@/types';
const CarDataTable = () => {
  const [data, setData] = useState<CarData[]>([]);
  const [vehicleId, setVehicleId] = useState('');
  const [amount, setAmount] = useState('');
  const { token, type } = getAuthDetails();
  const validToken = token ?? '';
  const validType = type ?? '';

  const handleSearch = async () => {
    if (!vehicleId || !amount) {
      alert('Por favor, complete ambos campos.');
      return;
    }
    try {
      const fetchedData = await fetchCarData(validToken, validType, parseInt(vehicleId), parseInt(amount));
      setData(fetchedData);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <input type="number" placeholder="Vehicle ID" value={vehicleId} onChange={(e) => setVehicleId(e.target.value)} />
      <input type="number" placeholder="Amount" value={amount} onChange={(e) => setAmount(e.target.value)} />
      <button onClick={handleSearch}>Buscar</button>
      <table className="table">
      <thead>
        <tr>
          <th>Date</th>
          <th>Fuel</th>
          <th>Latitude</th>
          <th>Longitude</th>
          <th>Speed</th>
        </tr>
      </thead>
      <tbody>
        {data.map((item, index) => (
          <tr key={index}>
            <td>{item.date}</td>
            <td>{item.fuel}</td>
            <td>{item.latitude}</td>
            <td>{item.longitude}</td>
            <td>{item.speed}</td>
          </tr>
        ))}
      </tbody>
    </table>
    </div>
  );
};

export default CarDataTable;
