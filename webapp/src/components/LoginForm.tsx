'use client';
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { loginUser } from '@/services/authService';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faLock } from '@fortawesome/free-solid-svg-icons';


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
            localStorage.setItem('token', result.data.access_token); 
        }
        if(result.data.access_token){
          router.push('/dashboard/map'); 
        }
    }).catch(error => {
        setError('Ocurrió un error inesperado durante el login.');
    });
  };

  return (
    <div className="login-form-container" style={{ width: '300px', margin: '100px auto', background: '#fff', padding: '20px', borderRadius: '8px', boxShadow: '0 4px 8px rgba(0,0,0,0.1)' }}>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="username">Usuario</label>
          <div className="input-group">
            <span className="input-group-text"><FontAwesomeIcon icon={faUser} /></span>
            <input
              type="text"
              id="username"
              className="form-control"
              placeholder="Usuario"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
        </div>
        <div className="form-group" style={{ marginTop: '10px' }}>
          <label htmlFor="password">Contraseña</label>
          <div className="input-group">
            <span className="input-group-text"><FontAwesomeIcon icon={faLock} /></span>
            <input
              type="password"
              id="password"
              className="form-control"
              placeholder="Contraseña"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
        </div>
        <button type="submit" className="btn btn-primary" style={{ marginTop: '20px', width: '100%', backgroundColor: '#6200EE', borderColor: '#6200EE' }}>Ingresar</button>
      </form>
    </div>
  );
};

export default LoginForm;
