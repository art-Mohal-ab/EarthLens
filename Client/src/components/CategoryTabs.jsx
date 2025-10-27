import React from 'react';
import './CategoryTabs.css';

const CategoryTabs = ({ selectedCategory, onCategoryChange }) => {
  const categories = [
    { id: 'all', label: 'All Actions' },
    { id: 'energy', label: 'Energy' },
    { id: 'water', label: 'Water' },
    { id: 'waste', label: 'Waste' },
    { id: 'transport', label: 'Transport' },
    { id: 'nature', label: 'Nature' }
  ];

  return (
    <div className="category-tabs">
      {categories.map(category => (
        <button
          key={category.id}
          className={`tab ${selectedCategory === category.id ? 'active' : ''}`}
          onClick={() => onCategoryChange(category.id)}
        >
          {category.label}
        </button>
      ))}
    </div>
  );
};

export default CategoryTabs;