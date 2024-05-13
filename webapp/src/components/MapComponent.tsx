import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polygon } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css'
import "leaflet-defaulticon-compatibility"
import "leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCar } from '@fortawesome/free-solid-svg-icons';

interface MapComponentProps {
  markers: [number, number][];
  names: string[];
  dates: string[];
}

const MapComponent: React.FC<MapComponentProps> = ({ markers, names, dates }) => {
  const [isClient, setIsClient] = useState(false);
  const size:number = 1
  useEffect(() => {
    setIsClient(true);
  }, []);

  if (!isClient) {
    return null; 
  }

  const mapStyle = {
    height: '70vh',
    width: '100%'
  };

  const polygon: [number, number][] = [
    [-17.41047981158394, -66.29267798176957],
    [-17.408693224961368, -66.27317424368415],
    [-17.39894113180513, -66.27294019882764],
    [-17.396720279198477, -66.23826774043988],
    [-17.37547885632445, -66.23879483880194],
    [-17.38268571477103, -66.29549818091319]
  ];

  const carIcon = new L.Icon({
    iconUrl: '/assets/icons_car.svg', 
    iconSize: [25, 25], 
    iconAnchor: [12, 4], 
    popupAnchor: [1, -5],  
  });

  return (
    <div>
      {isClient && (
        <MapContainer center={[-17.3927248,-66.2664538]} zoom={13.5} style={mapStyle}>
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />
          <Polygon positions={polygon} color="blue" />
            {markers.map((position, index) => (
              <Marker key={index} position={position} icon={carIcon}>
                <Popup>
                  {(markers[index][0].toFixed(6))}, {markers[index][1].toFixed(6)}
                  <br />
                  <b>Instructor: </b>{names[index]}<br/>
                  <b>Fecha: </b> {dates[index]}
                </Popup>
              </Marker>
            ))}
            
        </MapContainer>
      )}
    </div>
  );
};

export default MapComponent;
