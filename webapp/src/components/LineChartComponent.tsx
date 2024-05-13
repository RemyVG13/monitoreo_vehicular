import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Registro de los componentes necesarios de Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface DataPoint {
  x: string; // Suponiendo que 'x' es un string, por ejemplo una fecha
  y: number; // 'y' es un valor numérico
}

interface DataSet {
  name: string;
  data: DataPoint[];
}

interface CarLineChartProps {
  dataSets: DataSet[];
}

const options = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top' as const, // Tipo constante para cumplir con la expectativa de TypeScript
    },
    title: {
      display: true,
      text: 'Historial del Auto por Fechas',
    },
  },
  scales: {
    x: {
      display: false // No muestra las etiquetas en el eje x
    },
    y: {
      beginAtZero: true
    }
  }
};

export const CarLineChart: React.FC<CarLineChartProps> = ({ dataSets }) => {
  // Estructura de los datos para Chart.js
  const data = {
    labels: dataSets.length > 0 ? dataSets[0].data.map(d => d.x) : [],
    datasets: dataSets.map((set, index) => ({
      label: set.name,
      data: set.data.map(d => d.y),
      borderColor: getRandomColor(index), // Genera un color aleatorio
      backgroundColor: getRandomColor(index),
    })),
  };

  return <Line options={options} data={data} />;
};

// Función para generar un color aleatorio
function getRandomColor(index: number): string {
  const colors = [
    'rgba(255, 99, 132, 0.5)',
    'rgba(54, 162, 235, 0.5)',
    'rgba(255, 206, 86, 0.5)',
    'rgba(75, 192, 192, 0.5)',
    'rgba(153, 102, 255, 0.5)',
    'rgba(255, 159, 64, 0.5)',
    'rgba(199, 199, 199, 0.5)', // etc.
  ];
  return colors[index % colors.length]; // Cíclicamente selecciona un color
}
