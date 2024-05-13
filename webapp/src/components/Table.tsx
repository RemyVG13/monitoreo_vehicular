import React from 'react';
import { useRouter,usePathname } from "next/navigation";
import { BaseContentElement } from '@/types';
import { useState } from 'react';
import DeleteModal from './DeleteModal';


interface Column<T> {
  key: keyof T;
  label: string;
}

interface TableProps<T> {
  tableToken: string;
  tableType: string;
  columns: Column<T>[];
  data: T[];
  modalMessage: string;
  confirmDeleteModal: (token: string, type: string, term: string | null) => void;
}



function Table<T extends BaseContentElement>({ columns, data, modalMessage,confirmDeleteModal,tableToken,tableType}: TableProps<T>): JSX.Element {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const pathname = usePathname();
  const router = useRouter();

  const handleDeleteClick = (id: string) => {
    setSelectedId(id);
    setIsModalOpen(true);
  };

  const handleConfirmDelete = () => {
    console.log('Eliminar ID:', selectedId);
    setIsModalOpen(false);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  return (
    <div className="table-responsive">
      <table className="table table-striped">
        <thead>
          <tr>
            {columns.map((column, index) => (
              <th key={index}>{column.label}</th>
            ))}
            { tableToken !== "-" ?
                <th></th>
                :
                null
            }
            
          </tr>
        </thead>
        <tbody>
          {data.map((item, rowIndex) => (
            <tr key={rowIndex} onClick={() => router.push(`${pathname}/${item.id}`)}>
              {columns.map((column, colIndex) => (
                <td key={colIndex}>{item[column.key] ? String(item[column.key]) : ''}</td>
              ))}
              { tableToken !== "-" ?
                <td>
                  <button onClick={(e) => {
                    e.stopPropagation();
                    handleDeleteClick(item.id);
                  }} className="btn delete-table-btn">Eliminar</button>
                </td>
                :
                null
              }
              
            </tr>
          ))}
        </tbody>
      </table>
      <DeleteModal
        isOpen={isModalOpen}
        message={`${modalMessage} ${selectedId}?`}
        idDelete={selectedId}
        onClose={handleCloseModal}
        onConfirm={confirmDeleteModal}
        modalToken={tableToken}
        modalType={tableType}
      />

    </div>
  );
}

export default Table;

