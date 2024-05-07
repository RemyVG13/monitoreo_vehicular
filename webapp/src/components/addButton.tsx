import React from 'react';

interface AddButtonProps {
    onClick: () => void; // Define un tipo explícito para la función onClick
}

const AddButton: React.FC<AddButtonProps> = ({ onClick }) => {
    return (
        <button
            onClick={onClick}
            style={{
                padding: '10px 20px',
                background: '#007BFF',
                color: 'white',
                border: 'none',
                borderRadius: '5px',
                cursor: 'pointer',
                alignSelf: 'flex-end'
            }}
        >
            Añadir
        </button>
    );
};

export default AddButton;
