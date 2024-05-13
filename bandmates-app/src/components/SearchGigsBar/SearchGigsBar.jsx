import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './SearchGigsBar.css';

const SearchBar = ({ onFilterChange }) => {
  const [filters, setFilters] = useState({
    gigName: '',
    dateFrom: '',
    dateTo: '',
    instrument: '',
  });

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
    onFilterChange({ ...filters, [name]: value }); // This ensures the parent state is updated immediately
  };

  return (
    <div className="search-bar">
      <div className="search-bar-card">
        <h1>Search Gig</h1>
        <div className='search-bar-field'>
          <input
            type="text"
            name="gigName"
            placeholder="Search by gig name"
            value={filters.gigName}
            onChange={handleFilterChange}
          />
        </div>
        <div className='search-bar-field'>
          <input
            type="date"
            name="dateFrom"
            value={filters.dateFrom}
            onChange={handleFilterChange}
            placeholder="From date"
          />
        </div>
        <div className='search-bar-field'>
          <input
            type="date"
            name="dateTo"
            value={filters.dateTo}
            onChange={handleFilterChange}
            placeholder="To date"
          />
        </div>
        <div className='search-bar-field'>
          <input
            type="text"
            name="instrument"
            placeholder="Search by instrument"
            value={filters.instrument}
            onChange={handleFilterChange}
          />
        </div>
      </div>
    </div>
  );
};

SearchBar.propTypes = {
  onFilterChange: PropTypes.func.isRequired,
};

export default SearchBar;
