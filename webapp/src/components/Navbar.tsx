"use client"
import Link from 'next/link';
import { useRouter, usePathname } from "next/navigation";
import Image from 'next/image'

const Navbar = () => {
    const router = useRouter();
    const pathname = usePathname();
    const menuItems = [
        { name: "Mapa", path: "/dashboard/map" },
        { name: "Instructores", path: "/dashboard/teachers" },
        { name: "Autos", path: "/dashboard/cars" },
        { name: "Horarios", path: "/dashboard/schedules" },
        { name: "Reportes", path: "/dashboard/reports" },
        { name: "Alarmas", path: "/dashboard/alarms" }
    ];
    
    const handleLogout = () => {
        localStorage.removeItem('token');
        router.push('/login');
    };

    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark" style={{ backgroundColor: '#343a40' }}>
            <div className="container-fluid">
                <a className="navbar-brand">
                    <Image src="/assets/steering.svg" alt="Steering Wheel" width={40} height={40} />
                    <span style={{ marginLeft: '10px', color: '#BDC1CA', fontSize: '24px', fontWeight: 'bold' }}>General Motors</span>
                </a>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
                    <div className="navbar-nav mr-auto">
                        {menuItems.map((item, index) => (
                            <Link key={index} href={item.path} passHref  className={`nav-link ${pathname === item.path ? 'active' : ''}`} style={{ color: pathname === item.path ? '#15ABFF' : '#BDC1CA' }} aria-current="page">
                                {item.name}
                            </Link>
                        ))}
                    </div>
                    <button className="btn btn-danger ms-auto" onClick={handleLogout}>Salir</button>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
