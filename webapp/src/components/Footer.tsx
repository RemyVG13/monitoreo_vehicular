"use client"
import Link from 'next/link';
import { useRouter, usePathname } from "next/navigation";

const Footer = () => {
    const router = useRouter();

    return (
        <footer className="bg-body-tertiary text-center text-lg-start ">
            <div className="text-center p-3 bg-dark text-white" >
                © 2024 Copyright: Instituto Tecnológico General Motors
            </div>
        </footer>
    );
};

export default Footer;