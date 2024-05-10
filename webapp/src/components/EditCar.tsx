"use client";
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { fetchCar, updateCar } from '@/services/carService';
import { FormDataObject } from '@/types';

interface EditCarProps {
    car_id: string | null;
    backToCars: () => void;
    editToken: string;
    editType: string;
}

const EditCar = ({ car_id, backToCars, editToken, editType }: EditCarProps) => {
    const router = useRouter();
    const id = car_id;
    const [error, setError] = useState<string | null>(null);
    const [car, setCar] = useState({
        name: '',
        plate: '',
        make: '',
        model: '',
        year: '',
        thingspeak_id: '',
    });

    useEffect(() => {
        if (id) {
            fetchCarData(id);
        }
    }, [id]);

    const fetchCarData = async (carId: string) => {
        const data = await fetchCar(editToken, editType, carId);
        if (data) {
            setCar({
                name: data.name,
                plate: data.plate,
                make: data.make,
                model: data.model,
                year: data.year.toString(),
                thingspeak_id: data.thingspeak_id,
            });
        }
    };

    const handleSave = async () => {
        setError(null);
        const formData: FormDataObject = {
            name: car.name,
            plate: car.plate,
            make: car.make,
            model: car.model,
            year: parseInt(car.year),
            thingspeak_id: car.thingspeak_id,
        };
        try {
            const response = await updateCar(editToken, editType, id, formData);
            if (response !== "OK") {
                setError(response);
            } else {
                setError(null);
                router.push('/dashboard/cars');
            }
        } catch (error) {
            console.error('Error updating car:', error);
            setError('Failed to update car');
        }
    };

    const handleCancel = () => {
        router.push('/dashboard/cars');
    };

    return (
        <div className="container mt-5">
            <h2>Editar Auto</h2>
            <br />
            {error && <div className="alert alert-danger">{error}</div>}
            <div className="mb-3">
                <label htmlFor="name" className="form-label"><b>Nombre</b></label>
                <input type="text" className="form-control" id="name" value={car.name} onChange={e => setCar({ ...car, name: e.target.value })} />
            </div>
            <div className="mb-3">
                <label htmlFor="plate" className="form-label"><b>Matrícula</b></label>
                <input type="text" className="form-control" id="plate" value={car.plate} onChange={e => setCar({ ...car, plate: e.target.value })} />
            </div>
            <div className="mb-3">
                <label htmlFor="make" className="form-label"><b>Marca</b></label>
                <input type="text" className="form-control" id="make" value={car.make} onChange={e => setCar({ ...car, make: e.target.value })} />
            </div>
            <div className="mb-3">
                <label htmlFor="model" className="form-label"><b>Modelo</b></label>
                <input type="text" className="form-control" id="model" value={car.model} onChange={e => setCar({ ...car, model: e.target.value })} />
            </div>
            <div className="mb-3">
                <label htmlFor="year" className="form-label"><b>Año</b></label>
                <input type="number" className="form-control" id="year" value={car.year} onChange={e => setCar({ ...car, year: e.target.value })} />
            </div>
            <div className="mb-3">
                <label htmlFor="thingspeak_id" className="form-label"><b>ThingSpeak ID</b></label>
                <input type="text" className="form-control" id="thingspeak_id" value={car.thingspeak_id} onChange={e => setCar({ ...car, thingspeak_id: e.target.value })} />
            </div>
            <button onClick={handleSave} className="btn btn-primary">Guardar</button>
            <button onClick={handleCancel} className="btn btn-secondary">Volver</button>
        </div>
    );
};

export default EditCar;
