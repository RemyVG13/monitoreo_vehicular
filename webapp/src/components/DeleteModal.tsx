import React from 'react';

interface DeleteModalProps {
    isOpen: boolean;
    message: string;
    idDelete: string | null;
    onClose: () => void;
    onConfirm: (token: string, type: string, term: string | null) => void;
    modalToken: string;
    modalType: string;
  }



function DeleteModal({ isOpen, message, idDelete, onClose, onConfirm, modalToken,modalType}: DeleteModalProps) {


  if (!isOpen) return null;

  return (
    <div className={`modal ${isOpen ? 'show' : ''}`} tabIndex={-1} style={{ display: isOpen ? 'block' : 'none' }}>
      <div className="modal-dialog">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Confirmar Acción</h5>
            <button type="button" className="btn-close" onClick={onClose}></button>
          </div>
          <div className="modal-body">
            {message}
          </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Cancelar
            </button>
            <button type="button" className="btn btn-danger" onClick={() => {
              onConfirm(modalToken,modalType,idDelete);
              onClose();
            }}>
              Confirmar
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DeleteModal;
