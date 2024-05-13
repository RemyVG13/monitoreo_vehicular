import React, { useState, useEffect } from 'react';
import { fetchAllCars, fetchMapCar } from '@/services/carService';
import { Car, MapCarDetail } from '@/types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCarSide } from '@fortawesome/free-solid-svg-icons';
import { useRouter } from 'next/navigation';
import { MapContainer } from 'react-leaflet';
import { start } from 'repl';
import { useRef } from 'react';
 

interface CarMapDetailProps {
  carToken: string;
  carType: string;
  setcoords: (msg: [number, number][],msg2: string[],msg3: string[]) => void;
}

const CarMapDetail: React.FC<CarMapDetailProps> = ({ carToken, carType, setcoords}) => {
    const router = useRouter();
    const startCarIdRef = useRef<string>("");
    const [cars, setCars] = useState<Car[]>([]);
    const [selectedCar, setSelectedCar] = useState<MapCarDetail | null>(null);
    const [search, setSearch] = useState('');
    const [showDropdown, setShowDropdown] = useState(false);

    useEffect(() => {
        if (search.length > 0) {
        fetchAllCars(carToken, carType, search).then(setCars).catch(console.error);
        setShowDropdown(true);
        } else {
        setCars([]);
        setShowDropdown(false);
        }
    }, [search, carToken, carType]);

    const setCoords = async () => {
        try {
            console.log("startCarId",startCarIdRef.current)
            if (startCarIdRef.current){
                const mapCarDetails = await fetchMapCar(carToken, carType, startCarIdRef.current);
                mapCarDetails? setcoords(
                    [[mapCarDetails.latitude,mapCarDetails.longitude]],
                    [mapCarDetails.teacher_name],
                    [mapCarDetails.last_time]
                )
                    : console.log("No hay informacion");
                setSelectedCar(mapCarDetails);
                console.log("Fetching data...");
                console.log('Data fetched:', mapCarDetails);
            }else{
                console.log("No hay ID")
            }
            
            
        } catch (error) {
            console.error('Failed to fetch data:', error);
        }
    };

    useEffect(() => {
        const intervalId = setInterval(() => {
            setCoords();
        }, 5000);

        return () => clearInterval(intervalId);
    }, []);

    const selectCar = async (car: Car) => {
        console.log("car.id",car.id)
        const mapCarDetails = await fetchMapCar(carToken, carType, car.id);
        console.log("mapCarDetails",mapCarDetails)
        startCarIdRef.current = car.id;
        setSelectedCar(mapCarDetails);
        setShowDropdown(false);
    };

return (
    <div style={{marginTop: '20px', marginLeft: '10px', marginBottom: '20px'}}>
        <h3 style={{marginBottom:'10px', marginTop:'10px'}}>
            <b>Vehículos</b>
        </h3>
        <input
        type="search"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        placeholder="Buscar vehículo..."
        />
        {showDropdown && (
        <div>
            {cars.map((car) => (
            <div key={car.id} onClick={() => selectCar(car)}>
                {car.name}
            </div>
            ))}
        </div>
        )}
        {selectedCar && (
        <div>
            <br />
            <div className='container-fluid'>
                <div className='row'>
                    <div className='col-3 col-sm-2 col-lg-3'>
                        <FontAwesomeIcon icon={faCarSide} style={{
                        border: '2px solid MediumAquamarine',
                        backgroundColor: 'Gainsboro', 
                        borderRadius: '50%',
                        padding: '10px', 
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: 36
                    }} />
                    </div>
                    <div className='col-8 col-sm-10 col-lg-9 car-detail-title' style={{marginTop:'15px'}}>
                        {selectedCar.name}
                    </div>
                </div>
            </div>
            <br />

            <div style={{marginLeft:'30px'}}>
                <div className='car-detail-name'>Vehículo</div>
                <div style={{marginLeft:'10px'}} className='car-detail-content'>{selectedCar.make} {selectedCar.model} {selectedCar.year} {selectedCar.plate}</div>
            </div>
            <br />
            {selectedCar.is_working == "" && (
                <div style={{marginLeft:'30px'}}>
                    <br />
                    <div className='car-detail-name'>Este vehículo no está en horario de clases</div> 
                    <br />          
                </div>
                
            )}
            {selectedCar.is_working !== "" && (
                <div style={{marginLeft:'30px'}}>
                    <div className='car-detail-name'>Instructor</div>
                    <div className='car-detail-content' style={{marginLeft:'10px'}}>{selectedCar.teacher_name}</div>           
                </div>
            )}
            <br />
            <div style={{marginLeft:'30px'}}>
                <div className='car-detail-name'>Combustible</div>
                <div className='car-detail-content' style={{marginLeft:'10px'}}>{selectedCar.fuel} L</div>
                <br />
                <div className='car-detail-name'>Velocidad</div>
                <div className='car-detail-content' style={{marginLeft:'10px'}}>{selectedCar.speed} Km/h</div>
                <br />
                {selectedCar.state == "Activo" && (
                    <div>
                        <div className='car-detail-name'>Estado</div>
                        <div className='car-detail-content' style={{marginLeft:'10px'}}>{selectedCar.state}</div>        
                    </div>
                )}
                {selectedCar.state == "Inactivo" && (
                    <div >
                        <div className='car-detail-name'>Estado</div>
                        <div className='car-detail-content' style={{marginLeft:'10px'}}>{selectedCar.state}. Última conexión: {selectedCar.last_time}</div>        
                    </div>
                )}
                <br />
                <div className='car-detail-name'>Zona</div>
                <div className='car-detail-content' style={{marginLeft:'10px'}}>{selectedCar.zone}</div>           
            </div>
            
            <br />
            <button
                onClick={() => router.push(`/dashboard/map/history/${selectedCar.id}`)}
                style={{
                    backgroundColor: '#007BFF',
                    color: 'white',
                    border: 'none',
                    borderRadius: '20px',
                    padding: '10px 20px', 
                    fontSize: '16px',
                    cursor: 'pointer', 
                    outline: 'none'
                }}
                >
                Historial
            </button>

        </div>
        )}
    </div>
);
};

export default CarMapDetail;
