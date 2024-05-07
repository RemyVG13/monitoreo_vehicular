"use client"
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import { useEffect } from 'react';
import { useRouter } from "next/navigation";

const DashboardLayout = ({ children }: { children: React.ReactNode }) => {
    const router = useRouter();

    useEffect(() => {
        const token = localStorage.getItem("token") || "";
        if (!token) {
            router.push('/login'); // Redirige si no hay token
        }
    }, []); // Ejecuta solo una vez al montar el componente

    return (
        <div className="d-flex flex-column min-vh-100">
            <Navbar />

                <div className="flex-grow-1 bg-primary bg-opacity-10 ">{children}</div>

            <Footer />
        </div>
    );
}

export default DashboardLayout;
