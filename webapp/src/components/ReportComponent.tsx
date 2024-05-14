import React, { useState, useEffect } from 'react';
import { fetchReport } from '@/services/reportService';
import { fetchAllCars } from '@/services/carService';
import { Car } from '@/types';
import { useRouter } from 'next/navigation';
import { Report } from '@/types';
interface ReportComponentProps {
  carToken: string;
  carType: string;
  setReports: (rep: Report[]) => void;
}

const ReportComponent: React.FC<ReportComponentProps> = ({ carToken, carType, setReports }) => {
  const [criterion, setCriterion] = useState<string>('Distancia');
  const [vehicles, setVehicles] = useState<Car[]>([]);
  const [selectedVehicles, setSelectedVehicles] = useState<Car[]>([]);
  const [selectedVehicle, setSelectedVehicle] = useState<string>('');
  const [startDate, setStartDate] = useState<string>(new Date(Date.now() - 86400000).toISOString().substring(0, 16));
  const [endDate, setEndDate] = useState<string>(new Date().toISOString().substring(0, 16));
  const [period, setPeriod] = useState<string>('Día');
  const router = useRouter();

  useEffect(() => {
    const fetchCars = async () => {
      try {
        const cars = await fetchAllCars(carToken, carType, '');
        setVehicles(cars);
        if (cars.length > 0) {
          setSelectedVehicle(cars[0].id);
        }
      } catch (error) {
        console.error('Error fetching cars:', error);
      }
    };
    fetchCars();
  }, [carToken, carType]);

  const handleAddVehicle = () => {
    const car = vehicles.find(car => car.id === selectedVehicle);
    if (car && !selectedVehicles.includes(car)) {
      setSelectedVehicles([...selectedVehicles, car]);
    }
  };

  const handleRemoveVehicle = (car: Car) => {
    setSelectedVehicles(selectedVehicles.filter(v => v.id !== car.id));
  };

  const formatDate = (date: string) => {
    return new Date(date).toISOString().split('.')[0] + 'Z';
  };

  const handleApply = async () => {
    try {
      const results = [];
      for (const car of selectedVehicles) {
        const result = await fetchReport(carToken, carType, car.id, formatDate(startDate), formatDate(endDate), period, criterion);
        results.push(result);
      }
      console.log(results);
      setReports(results)
    } catch (error) {
      console.error('Error fetching reports:', error);
    }
  };

  const handleClear = () => {
    setSelectedVehicles([]);
    setCriterion('Distancia');
    setStartDate(new Date(Date.now() - 86400000).toISOString().substring(0, 16));
    setEndDate(new Date().toISOString().substring(0, 16));
    setPeriod('Día');
  };

  return (
    <div className="report-component">
      <div className="form-group">
        <label>Criterio</label>
        <select value={criterion} onChange={e => setCriterion(e.target.value)}>
          <option value="Distancia">Distancia Recorrida en Km</option>
          <option value="Combustible">Combustible consumido en L </option>
        </select>
      </div>

      <div className="form-group">
        <label>Vehículos</label>
        <select value={selectedVehicle} onChange={e => setSelectedVehicle(e.target.value)}>
          {vehicles.map(car => (
            <option key={car.id} value={car.id}>{car.name}</option>
          ))}
        </select>
        <br />
        <button style={{margin: '10px'}} onClick={handleAddVehicle}>Añadir</button>
        <br />
        <div className="tags">
          {selectedVehicles.map(car => (
            <div key={car.id} className="tag">
              {car.name} <span onClick={() => handleRemoveVehicle(car)}>×</span>
            </div>
          ))}
        </div>
      </div>

      <div className="form-group">
        <label>Rango de fechas</label>
        <input type="datetime-local" value={startDate} onChange={e => setStartDate(e.target.value)} />
        <input type="datetime-local" value={endDate} onChange={e => setEndDate(e.target.value)} />
      </div>

      <div className="form-group">
        <label>Periodo</label>
        <select value={period} onChange={e => setPeriod(e.target.value)}>
          <option value="Hora">Hora</option>
          <option value="Día">Día</option>
          <option value="Mes">Mes</option>
          <option value="Semana">Semana</option>
          <option value="Año">Año</option>
        </select>
      </div>

      <div className="form-group">
        <button onClick={handleApply}>Aplicar</button>
        <button onClick={handleClear}>Limpiar</button>
      </div>
    </div>
  );
};

export default ReportComponent;
