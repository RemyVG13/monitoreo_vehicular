import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';

interface SearchBarProps {
    onSearch: (term: string) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch }) => {
    const [searchTerm, setSearchTerm] = useState('');

    const handleSearch = (event: React.FormEvent) => {
        event.preventDefault();
        onSearch(searchTerm);
    };

    return (
        <form onSubmit={handleSearch} style={{ display: 'flex' }}>
            <input
                type="text"
                placeholder="Buscar..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                style={{
                    flex: 1,
                    padding: '10px',
                    border: '1px solid #ccc',
                    borderTopLeftRadius: '5px',
                    borderBottomLeftRadius: '5px'
                }}
            />
            <button type="submit" style={{
                padding: '10px',
                background: '#007BFF',
                color: 'white',
                border: 'none',
                borderTopRightRadius: '5px',
                borderBottomRightRadius: '5px',
                cursor: 'pointer'
            }}>
                <FontAwesomeIcon icon={faSearch} />
            </button>
        </form>
    );
};

export default SearchBar;
