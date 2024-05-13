import React, { useState, useEffect } from 'react';
import { fetchAllCars, fetchHistoryCar } from '@/services/carService';
import { Car } from '@/types';
import { HistoryData } from '@/types';
interface CarSearchProps {
  carToken: string;
  carType: string;
  carId?: string;
  setWayPoints: (msg: [number, number][],msg2: string[],msg3: string[]) => void;
}

const CarSearch: React.FC<CarSearchProps> = ({ carToken, carType, carId = "",setWayPoints }) => {
  const [cars, setCars] = useState<Car[]>([]);
  const [selectedCarId, setSelectedCarId] = useState<string>(carId);
  const today = new Date();
  const yesterday = new Date(today);
  yesterday.setDate(today.getDate() - 1);
  const formatDate = (date: Date) => date.toISOString().slice(0, 16);

  const [startDate, setStartDate] = useState<string>(formatDate(yesterday));
  const [endDate, setEndDate] = useState<string>(formatDate(today));

  useEffect(() => {
    fetchAllCars(carToken, carType, "").then(setCars).catch(console.error);
  }, [carToken, carType]);

  const handleApply = async () => {
    if (new Date(startDate) > new Date(endDate)) {
      alert("La fecha final no puede ser anterior a la fecha inicial.");
      return;
    }
    const historyData : HistoryData = await fetchHistoryCar(carToken, carType, selectedCarId, startDate, endDate);
    historyData? setWayPoints(
        historyData.coords_list,
        historyData.teacher_name_list,
        historyData.dates_list
        
    ) 
    : console.log("No data")
    console.log(historyData);
  };

  return (
    <div style={{margin: "30px"}}>
        <div className='container-fluid'>
            <div className='row'>

            <select value={selectedCarId} onChange={e => setSelectedCarId(e.target.value)}>
                {cars.map((car) => (
                <option key={car.id} value={car.id}>{car.name}</option>
                ))}
            </select>
            
            </div>
                <br />
            <div className='row'>
                <div className='col-5'>
                    Desde: 
                    <input type="datetime-local" value={startDate} onChange={e => setStartDate(e.target.value)} />
                </div>
            </div>
            <br />

            <div className='row'>
                <div className='col-5'>
                    Hasta:
                    <input type="datetime-local" value={endDate} onChange={e => setEndDate(e.target.value)} />
                </div>
            </div>
            <br />
            <button onClick={handleApply}>Aplicar</button>

        </div>

    </div>
  );
};

export default CarSearch;
