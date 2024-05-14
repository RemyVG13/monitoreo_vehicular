import React, { useState, useEffect } from 'react';
import { fetchAllCars, fetchHistoryCar } from '@/services/carService';
import { Car, HistoryData } from '@/types';

interface CarSearchProps {
  carToken: string;
  carType: string;
  carId?: string;
  setWayPoints: (msg: [number, number][], msg2: string[], msg3: string[]) => void;
}

const CarSearch: React.FC<CarSearchProps> = ({ carToken, carType, carId = "", setWayPoints }) => {
  const [cars, setCars] = useState<Car[]>([]);
  const [selectedCarId, setSelectedCarId] = useState<string>(carId);
  const utcDate = new Date(); // Obtiene la fecha y hora actual en UTC
  const todayBolivia = new Date(utcDate.getTime() - 4 * 3600000);
  const yesterdayBolivia = new Date(todayBolivia);
  yesterdayBolivia.setDate(todayBolivia.getDate() - 1);
  const formatDate = (date: Date) => date.toISOString().slice(0, 16);

  const [startDate, setStartDate] = useState<string>(formatDate(yesterdayBolivia));
  const [endDate, setEndDate] = useState<string>(formatDate(todayBolivia));

  useEffect(() => {
    fetchAllCars(carToken, carType, "").then(setCars).catch(console.error);
  }, [carToken, carType]);

  const handleApply = async () => {
    if (new Date(startDate) > new Date(endDate)) {
      alert("La fecha final no puede ser anterior a la fecha inicial.");
      return;
    }
    const historyData: HistoryData = await fetchHistoryCar(carToken, carType, selectedCarId, startDate, endDate);
    if (historyData) {
      setWayPoints(
        historyData.coords_list,
        historyData.teacher_name_list,
        historyData.dates_list
      );
    } else {
      console.log("No data");
    }
    console.log(historyData);
  };

  return (
    <div className="car-search">
      <div className="form-group">
        <label>Vehículos</label>
        <select value={selectedCarId} onChange={e => setSelectedCarId(e.target.value)}>
          {cars.map((car) => (
            <option key={car.id} value={car.id}>{car.name}</option>
          ))}
        </select>
      </div>
      <div className="form-group">
        <label>Desde</label>
        <input type="datetime-local" value={startDate} onChange={e => setStartDate(e.target.value)} />
      </div>
      <div className="form-group">
        <label>Hasta</label>
        <input type="datetime-local" value={endDate} onChange={e => setEndDate(e.target.value)} />
      </div>
      <div className="form-group">
        <button className="apply-button" onClick={handleApply}>Aplicar</button>
      </div>
    </div>
  );
};

export default CarSearch;
