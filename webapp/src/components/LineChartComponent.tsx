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

interface Report {
  car_name: string;
  report_type: string;
  report: [string, number][];
}

interface CarLineChartProps {
  reports: Report[];
}

const options = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top' as const,
    },
    title: {
      display: true,
      text: 'Historial del Auto por Fechas',
    },
    tooltip: {
      callbacks: {
        title: (tooltipItems: any) => {
          return tooltipItems[0].label; // Muestra la fecha como título del tooltip
        },
      },
    },
  },
  scales: {
    x: {
      display: false, // No muestra las etiquetas en el eje x
    },
  },
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

function normalizeReports(reports: Report[]): Report[] {
  // Recopila todas las fechas únicas de todos los reportes
  const allDates = new Set<string>();
  reports.forEach(report => {
    report.report.forEach(([date]) => {
      allDates.add(date);
    });
  });

  const sortedDates = Array.from(allDates).sort((a, b) => new Date(a).getTime() - new Date(b).getTime());

  // Normaliza cada reporte
  return reports.map(report => {
    const normalizedReport: [string, number][] = sortedDates.map(date => {
      const found = report.report.find(([reportDate]) => reportDate === date);
      return found ? found : [date, 0];
    });

    return {
      ...report,
      report: normalizedReport,
    };
  });
}


export const CarLineChart: React.FC<CarLineChartProps> = ({ reports }) => {
  const normalizedReports = normalizeReports(reports);

  // Preparar los datos para Chart.js
  const data = {
    labels: normalizedReports.length > 0 ? normalizedReports[0].report.map((item) => item[0]) : [],
    datasets: normalizedReports.map((report, index) => ({
      label: report.car_name,
      data: report.report.map((item) => item[1]),
      borderColor: getRandomColor(index), // Genera un color del arreglo finito
      backgroundColor: getRandomColor(index),
    })),
  };

  return <Line options={options} data={data} />;
};
