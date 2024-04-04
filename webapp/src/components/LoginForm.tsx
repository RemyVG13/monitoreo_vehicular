'use client';
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { loginUser } from '@/services/authService';

const LoginForm = () => {
  const router = useRouter();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    loginUser(username, password).then(result => {
        if (!result.success) setError(result.message);
        else {
            // Aquí manejas el éxito del login, por ejemplo, guardando el token
            localStorage.setItem('token', result.data.access_token); // Ajusta según tu respuesta
            router.push('/dashboard/cardata'); // Redirige a la página principal
        }
    }).catch(error => {
        setError('Ocurrió un error inesperado durante el login.');
    });
  };

  return (
    <div className="container mt-5">
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="username" className="form-label">Username</label>
          <input type="text" className="form-control" id="username" value={username} onChange={(e) => setUsername(e.target.value)} />
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label">Password</label>
          <input type="password" className="form-control" id="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </div>
        <button type="submit" className="btn btn-primary">Login</button>
        {error && <div className="alert alert-danger mt-3">{error}</div>}
      </form>
    </div>
  );
};

export default LoginForm;
