'use client';
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { fetchAllTeachers } from '@/services/teacherService';
import { fetchAllCars } from '@/services/carService';
import { fetchSchedule, updateSchedule} from '@/services/scheduleService';
import { Teacher, Car, FormDataObject } from '@/types';
import { getAuthDetails } from '@/utils/authUtils';

interface EditScheduleProps {
    schedule_id: string;
    backToSchedules: () => void;
    editToken: string;
    editType: string;
}

const EditSchedule = ({ schedule_id, backToSchedules, editToken, editType }: EditScheduleProps) => {
    const router = useRouter();
    const [schedule, setSchedule] = useState({
        teacher_id: '',
        car_id: '',
        day: '',
        time: '',  // This will handle time input
    });
    const [teachers, setTeachers] = useState<Teacher[]>([]);
    const [cars, setCars] = useState<Car[]>([]);
    const [error, setError] = useState('');

    useEffect(() => {
        const loadInitialData = async () => {
            try {
                const data = await fetchSchedule(editToken, editType, schedule_id);
                const fetchedTeachers = await fetchAllTeachers(editToken, editType, '');
                const fetchedCars = await fetchAllCars(editToken, editType, '');
                setTeachers(fetchedTeachers);
                setCars(fetchedCars);

                if (data) {
                    setSchedule({
                        teacher_id: data.teacher_id,
                        car_id: data.car_id,
                        day: data.day,
                        time: new Date(data.hour * 1000).toISOString().substring(11, 16),  // Convert seconds to HH:MM format
                    });
                }
            } catch (error) {
                console.error('Error loading schedule data:', error);
                setError('Failed to load data');
            }
        };

        loadInitialData();
    }, [editToken, editType, schedule_id]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setSchedule({ ...schedule, [name]: value });
    };

    const handleSubmit = async () => {
        setError('');
        // Convert time from HH:MM to seconds since midnight
        const [hours, minutes] = schedule.time.split(':').map(Number);
        const hourInSeconds = hours * 3600 + minutes * 60;
        const formData: FormDataObject = {
            teacher_id: schedule.teacher_id,
            car_id: schedule.car_id,
            day: schedule.day,
            hour: hourInSeconds,
        };

        console.log("FORMDATA");
        console.log(formData);

        try {
            const response = await updateSchedule(editToken, editType, schedule_id, formData);
            if (response !== "OK") {
                setError(response);
            } else {
                backToSchedules();
            }
        } catch (error) {
            console.error('Error updating schedule:', error);
            setError('Failed to update schedule');
        }
    };

    return (
        <div className="container mt-5">
            <h2>Editar Horario</h2>
            <br />
            {error && <div className="alert alert-danger">{error}</div>}
            <form>
                <div className="mb-3">
                    <label htmlFor="teacher_id" className="form-label"><b>Instructor</b></label>
                    <select className="form-select" name="teacher_id" value={schedule.teacher_id} onChange={handleChange}>
                        <option value="">Seleccionar instructor</option>
                        {teachers.map((teacher) => (
                            <option key={teacher.id} value={teacher.id}>
                                {teacher.first_name} {teacher.father_last_name}
                            </option>
                        ))}
                    </select>
                </div>
                <div className="mb-3">
                    <label htmlFor="car_id" className="form-label"><b>Auto</b></label>
                    <select className="form-select" name="car_id" value={schedule.car_id} onChange={handleChange}>
                        <option value="">Seleccionar auto</option>
                        {cars.map((car) => (
                            <option key={car.id} value={car.id}>{car.name}</option>
                        ))}
                    </select>
                </div>
                <div className="mb-3">
                    <label htmlFor="day" className="form-label"><b>Día</b></label>
                    <input type="text" className="form-control" name="day" value={schedule.day} onChange={handleChange} />
                </div>
                <div className="mb-3">
                    <label htmlFor="time" className="form-label"><b>Hora (HH:MM)</b></label>
                    <input type="time" className="form-control" name="time" value={schedule.time} onChange={handleChange} />
                </div>
                <button type="button" onClick={handleSubmit} className="btn btn-primary">Guardar</button>
                <button type="button" onClick={backToSchedules} className="btn btn-secondary">Volver</button>
            </form>
        </div>
    );
};

export default EditSchedule;
