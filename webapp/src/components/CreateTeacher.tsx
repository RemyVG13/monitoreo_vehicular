'use client';
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { createTeacher } from '@/services/teacherService';
import { FormDataObject } from '@/types';
import { getAuthDetails } from '@/utils/authUtils';


interface CreateTeacherProps {
    backToTeachers: () => void;
    createToken: string;
    createType: string;
  }


const CreateTeacher = ({ backToTeachers, createToken,createType}: CreateTeacherProps) => {
  const router = useRouter();
  const { token, type } = getAuthDetails();

  const [teacher, setTeacher] = useState({
    firstName: '',
    lastNameFather: '',
    lastNameMother: '',
    idNumber: '',
    idZone: '',
    cellPhone: '',
    birthday: '',
  });

  const [error, setError] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setTeacher({ ...teacher, [name]: value });
  };
  

  const handleSubmit = async () => {
    setError('');
    const formData: FormDataObject = {
      first_name: teacher.firstName,
      father_last_name: teacher.lastNameFather,
      mother_last_name: teacher.lastNameMother,
      id_number: teacher.idNumber,
      id_zone: teacher.idZone,
      cellPhone: teacher.cellPhone,
      birthday_date_inseconds: new Date(teacher.birthday).getTime() / 1000,
    };

    try {
      const response = await createTeacher(createToken, createType, formData);
      if (response !== "OK") {
        setError(response);
      } else {
        router.push('/dashboard/teachers');
      }
    } catch (error) {
      console.error('Error creating teacher:', error);
      setError('Failed to create teacher');
    }
  };

  const handleCancel = () => {
    router.push('/dashboard/teachers');
  };

  return (
    <div className="container mt-5">
      <h2>Crear Nuevo Instructor</h2>
      <br />
      {error && <div className="alert alert-danger">{error}</div>}
      <form>
        <div className="mb-3">
            <label htmlFor="firstName" className="form-label"><b>Nombre</b></label>
            <input type="text" className="form-control" name="firstName" value={teacher.firstName} onChange={handleChange}  />
        </div>
        <div className="row">
            <div className="col">
                <label htmlFor="lastNameFather" className="form-label"><b>Apellido paterno</b></label>
                <input type="text" className="form-control" name="lastNameFather" value={teacher.lastNameFather} onChange={handleChange}  />
            </div>
            <div className="col">
                <label htmlFor="lastNameMother" className="form-label"><b>Apellido materno</b></label>
                <input type="text" className="form-control" name="lastNameMother" value={teacher.lastNameMother} onChange={handleChange}  />
            </div>
        </div>
        <div className="mb-3">
            <label htmlFor="idNumber" className="form-label"><b>Carnet</b></label>
            <input type="text" className="form-control" name="idNumber" value={teacher.idNumber} onChange={handleChange}  />
        </div>
        <div className="mb-3">
            <label htmlFor="idZone" className="form-label"><b>Zona</b></label>
            <input type="text" className="form-control" name="idZone" value={teacher.idZone} onChange={handleChange}  />
        </div>
        <div className="mb-3">
            <label htmlFor="cellPhone" className="form-label"><b>Celular</b></label>
            <input type="tel" className="form-control" name="cellPhone" value={teacher.cellPhone} onChange={handleChange}  />
        </div>
        <div className="mb-3">
            <label htmlFor="birthday" className="form-label"><b>Cumpleaños</b></label>
            <input
                type="date"
                className="form-control"
                name="birthday"
                value={teacher.birthday}
                onChange={handleChange} 
            />
        </div>
        <div className="mb-3">
          <button type="button" onClick={handleSubmit} className="btn btn-primary">Crear</button>
          <button type="button" onClick={handleCancel} className="btn btn-secondary">Volver</button>
        </div>
      </form>
    </div>
  );
};

export default CreateTeacher;
