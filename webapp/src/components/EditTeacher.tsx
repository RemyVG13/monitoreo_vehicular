"use client";
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { fetchTeacher, updateTeacher } from '@/services/teacherService';
import { FormDataObject } from '@/types';

interface EditTeacherProps {
    teacher_id: string | null;
    backToTeachers: () => void;
    editToken: string;
    editType: string;
  }

const EditTeacher = ({ teacher_id, backToTeachers, editToken,editType}: EditTeacherProps) => {
    const router = useRouter();
    const id  = teacher_id;
    const [error, setError] = useState<string | null>(null);
    const [teacher, setTeacher] = useState({
        firstName: '',
        lastNameFather: '',
        lastNameMother: '',
        idNumber: '',
        idZone: '',
        cellPhone: '',
        birthday: '',
    });

    useEffect(() => {
        if (id) {
            fetchTeacherData(id);
        }
    }, [id]);

    const fetchTeacherData = async (teacherId: string) => {
        const data = await fetchTeacher(editToken,editType, teacherId); 
        if (data) {
            setTeacher({
                firstName: data.first_name,
                lastNameFather: data.father_last_name,
                lastNameMother: data.mother_last_name,
                idNumber: data.id_number.toString(),
                idZone: data.id_zone,
                cellPhone: data.cellPhone,  // Asumiendo que este campo existe
                birthday: new Date(data.birthday_date_inseconds * 1000).toISOString().substring(0, 10),
            });
        }
    };

    const handleSave = async () => {
        setError(null);
        const formData: FormDataObject = {
            // Asume que los campos aquí son los que tu backend espera
            first_name: teacher.firstName,
            father_last_name: teacher.lastNameFather,
            mother_last_name: teacher.lastNameMother,
            id_number: teacher.idNumber,
            id_zone: teacher.idZone,
            cellPhone: teacher.cellPhone, // Asegúrate de que este campo exista en tu backend
            birthday_date_inseconds: new Date(teacher.birthday).getTime() / 1000,
        };
        try {
            
            const response = await updateTeacher(editToken,editType, id, formData);
            console.log("response");
            console.log(response);
            if (response !== "OK"){
                setError(response);
            }else{
                setError(null);
                router.push('/dashboard/teachers');
            }
            
        } catch (error) {
            console.error(error);
        }
        
        
    };

    const handleCancel = () => {
        router.push('/dashboard/teachers');
    };

    return (
        <div className="container mt-5">
            <h2>Editar Instructor</h2>
            <br />
            {error && <div className="alert alert-danger">{error}</div>}
            <div className="mb-3">
                <label htmlFor="firstName" className="form-label"><b>Nombre</b></label>
                <input type="text" className="form-control" id="firstName" value={teacher.firstName} onChange={e => setTeacher({...teacher, firstName: e.target.value})} />
            </div>
            <div className="row">
                <div className="col">
                    <label htmlFor="lastNameFather" className="form-label"><b>Apellido paterno</b></label>
                    <input type="text" className="form-control" id="lastNameFather" value={teacher.lastNameFather} onChange={e => setTeacher({...teacher, lastNameFather: e.target.value})} />
                </div>
                <div className="col">
                    <label htmlFor="lastNameMother" className="form-label"><b>Apellido materno</b></label>
                    <input type="text" className="form-control" id="lastNameMother" value={teacher.lastNameMother} onChange={e => setTeacher({...teacher, lastNameMother: e.target.value})} />
                </div>
            </div>
            <div className="mb-3">
                <label htmlFor="idNumber" className="form-label"><b>Carnet</b></label>
                <input type="text" className="form-control" id="idNumber" value={teacher.idNumber} onChange={e => setTeacher({...teacher, idNumber: e.target.value})} />
            </div>
            <div className="mb-3">
                <label htmlFor="idZone" className="form-label"><b>Zona</b></label>
                <input type="text" className="form-control" id="idZone" value={teacher.idZone} onChange={e => setTeacher({...teacher, idZone: e.target.value})} />
            </div>
            <div className="mb-3">
                <label htmlFor="cellPhone" className="form-label"><b>Celular</b></label>
                <input type="tel" className="form-control" id="cellPhone" value={teacher.cellPhone} onChange={e => setTeacher({...teacher, cellPhone: e.target.value})} />
            </div>
            <div className="mb-3">
                <label htmlFor="birthday" className="form-label"><b>Cumpleaños</b></label>
                <input
                    type="date"
                    className="form-control"
                    id="birthday"
                    value={teacher.birthday}
                    onChange={e => setTeacher({...teacher, birthday: e.target.value})}
                />
            </div>
            <button onClick={handleSave} className="btn btn-primary">Guardar</button>
            <button onClick={handleCancel} className="btn btn-secondary">Volver</button>
        </div>
    );
};

export default EditTeacher;
