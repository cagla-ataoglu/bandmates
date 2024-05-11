import React, { useState } from 'react';
import PropTypes from 'prop-types'; // Import PropTypes
import './SearchGigsBar.css'; // Import CSS file

const SearchBar = ({ onSearch, onFilterChange }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    date: '',
    place: '',
    instrument: '',
  });

  const handleSearch = () => {
    onSearch(searchTerm);
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters({ ...filters, [name]: value });
    onFilterChange(filters);
  };

  return (
    <div className="search-bar">
        <div className="search-bar-card">
            <h1>Search Gig</h1>
        <input
            type="text"
            placeholder="Search by name"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
        />
        <select name="date" onChange={handleFilterChange}>
            <option value="">Select Date</option>
            {/* Add options for dates */}
        </select>
        <select name="place" onChange={handleFilterChange}>
            <option value="">Select Place</option>
            {/* Add options for places */}
        </select>
        <select name="instrument" onChange={handleFilterChange}>
            <option value="">Select Instrument</option>
            {/* Add options for instruments */}
        </select>
      </div>
      <button onClick={handleSearch}>Search</button>
    </div>
  );
};

// Prop type validation
SearchBar.propTypes = {
  onSearch: PropTypes.func.isRequired,
  onFilterChange: PropTypes.func.isRequired,
};

export default SearchBar;
