
'use client';
import LoginForm from '@/components/LoginForm'; // Asegúrate de que el path sea correcto
import Image from 'next/image';

const LoginPage = () => {
  return (
    <div className="login-page">
      <div className="overlay"></div> {/* Overlay para el color */}
      <div className="content">
        <div className="logo d-none d-md-block">
          <Image src="/assets/logo.svg" alt="Logo del Instituto" width={500} height={500} />
        </div>
        <div className="login-form">
          <LoginForm />
        </div>
      </div>
    </div>
  );
};

export default LoginPage;


