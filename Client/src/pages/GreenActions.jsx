import React, { useState, useEffect } from 'react';
import '../styles/GreenActions.css';
import ActionFeed from '../components/ActionFeed';
import CategoryTabs from '../components/CategoryTabs';

const GreenActions = () => {
  const [actions, setActions] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchGreenActions();
  }, []);

  const fetchGreenActions = async () => {
    try {
      const response = await fetch('http://localhost:5001/api/ai/green-advice');
      if (response.ok) {
        const data = await response.json();
        setActions(data.actions);
      }
    } catch (error) {
      console.error('Failed to fetch green actions:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredActions = selectedCategory === 'all' 
    ? actions 
    : actions.filter(action => action.category === selectedCategory);

  return (
    <div className="green-actions-container">
      <header className="green-actions-header">
        <h1>Green Actions</h1>
        <p>Discover eco-friendly actions to make a positive impact</p>
      </header>

      <CategoryTabs 
        selectedCategory={selectedCategory}
        onCategoryChange={setSelectedCategory}
      />

      <ActionFeed 
        actions={filteredActions}
        loading={loading}
      />
    </div>
  );
};

export default GreenActions;