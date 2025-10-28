import React from 'react';

const FilterBar = ({ filters, onFilterChange }) => {
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    onFilterChange({ ...filters, [name]: value });
  };

  return (
    <div className="filter-bar">
      <div className="filter-group">
        <input
          type="text"
          name="location"
          placeholder="Filter by location..."
          value={filters.location || ''}
          onChange={handleInputChange}
          className="filter-input"
        />
        <select
          name="category"
          value={filters.category || ''}
          onChange={handleInputChange}
          className="filter-select"
        >
          <option value="">All Categories</option>
          <option value="Waste Management">Waste Management</option>
          <option value="Air Pollution">Air Pollution</option>
          <option value="Flooding">Flooding</option>
          <option value="Poaching">Poaching</option>
          <option value="Water Pollution">Water Pollution</option>
          <option value="Deforestation">Deforestation</option>
        </select>
      </div>
    </div>
  );
};

export default FilterBar;
