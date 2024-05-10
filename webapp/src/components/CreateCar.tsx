'use client';
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { createCar } from '@/services/carService';
import { Car, FormDataObject } from '@/types';
import { getAuthDetails } from '@/utils/authUtils';

interface CreateTeacherProps {
  backToCars: () => void;
  createToken: string;
  createType: string;
}

const CreateCar = ({ backToCars, createToken,createType}: CreateTeacherProps) => {
  const router = useRouter();

  const [car, setCar] = useState({
    name: '',
    plate: '',
    make: '',
    model: '',
    year: '',
    thingspeak_id: '',
  });
  const [error, setError] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setCar({ ...car, [name]: value });
  };

  const handleSubmit = async () => {
    setError('');
    const formData: FormDataObject = {
      name: car.name,
      plate: car.plate,
      make: car.make,
      model: car.model,
      year: car.year,
      thingspeak_id: car.thingspeak_id,
    };

    try {
      const response = await createCar(createToken, createType, formData);
      if (response !== "OK") {
        setError(response);
      } else {
        router.push('/dashboard/cars');
      }
    } catch (error) {
      console.error('Error creating car:', error);
      setError('Failed to create car');
    }
  };

  const handleCancel = () => {
    router.push('/dashboard/cars');
  };

  return (
    <div className="container mt-5">
      <h2>Crear Nuevo Auto</h2>
      <br />
      {error && <div className="alert alert-danger">{error}</div>}
      <form>
        <div className="mb-3">
          <label htmlFor="name" className="form-label"><b>Nombre</b></label>
          <input type="text" className="form-control" name="name" value={car.name} onChange={handleChange} />
        </div>
        <div className="mb-3">
          <label htmlFor="plate" className="form-label"><b>Matrícula</b></label>
          <input type="text" className="form-control" name="plate" value={car.plate} onChange={handleChange} />
        </div>
        <div className="mb-3">
          <label htmlFor="make" className="form-label"><b>Marca</b></label>
          <input type="text" className="form-control" name="make" value={car.make} onChange={handleChange} />
        </div>
        <div className="mb-3">
          <label htmlFor="model" className="form-label"><b>Modelo</b></label>
          <input type="text" className="form-control" name="model" value={car.model} onChange={handleChange} />
        </div>
        <div className="mb-3">
          <label htmlFor="year" className="form-label"><b>Año</b></label>
          <input type="number" className="form-control" name="year" value={car.year} onChange={handleChange} />
        </div>
        <div className="mb-3">
          <label htmlFor="thingspeak_id" className="form-label"><b>ThingSpeak ID</b></label>
          <input type="number" className="form-control" name="thingspeak_id" value={car.thingspeak_id} onChange={handleChange} />
        </div>
        <div className="mb-3">
          <button type="button" onClick={handleSubmit} className="btn btn-primary">Guardar</button>
          <button type="button" onClick={handleCancel} className="btn btn-secondary">Volver</button>
        </div>
      </form>
    </div>
  );
};

export default CreateCar;
