import React, { useState, useEffect } from 'react';
import '../styles/GreenActions.css';
import ActionFeed from '../components/ActionFeed';
import CategoryTabs from '../components/CategoryTabs';

const GreenActions = () => {
  const [actions, setActions] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [loading, setLoading] = useState(true);
  const [completedActions, setCompletedActions] = useState(new Set());

  useEffect(() => {
    fetchGreenActions();
  }, []);

  const fetchGreenActions = async () => {
    try {
      const response = await fetch('http://localhost:5001/api/ai/green-advice');
      if (response.ok) {
        const data = await response.json();
        console.log('API Response:', data);
        setActions(data.actions);
      } else {
        console.error('API Error:', response.status, response.statusText);
        // Fallback to mock data
        setActions(mockActions);
      }
    } catch (error) {
      console.error('Failed to fetch green actions:', error);
      // Fallback to mock data
      setActions(mockActions);
    } finally {
      setLoading(false);
    }
  };

  const mockActions = [
    {title: "Switch to LED Bulbs", category: "Energy", difficulty: "Easy", description: "Replace traditional bulbs with energy efficient LED lights throughout your home.", impact: "Saves 75% energy, reduces 200kg CO₂/year"},
    {title: "Collect Rainwater", category: "Water", difficulty: "Medium", description: "Set up rainwater harvesting system for watering plants and gardens.", impact: "Saves 500+ litres per month"},
    {title: "Plant Native Trees", category: "Nature", difficulty: "Medium", description: "Plant indigenous tree species in your community to restore ecosystem.", impact: "Absorb 20kg carbon dioxide per tree"},
    {title: "Start Composting", category: "Waste", difficulty: "Medium", description: "Turn food waste into nutrient-rich compost for gardening.", impact: "Diverts 150kg waste from landfills per year"},
    {title: "Install Solar Panels", category: "Energy", difficulty: "Hard", description: "Generate clean energy by installing solar panels on your roof.", impact: "Saves 3,000kgs carbon dioxide per year"},
    {title: "Fix Water Leaks", category: "Water", difficulty: "Easy", description: "Repair dripping taps and leaking pipes to conserve water.", impact: "Saves 20 litres per day"},
    {title: "Use Public Transport", category: "Lifestyle", difficulty: "Easy", description: "Choose buses, trains, or carpool instead of driving alone.", impact: "Reduces 1,000kg carbon dioxide per year"},
    {title: "Create Wildlife Habitat", category: "Nature", difficulty: "Medium", description: "Plant native flowers and shrubs to support local pollinators and birds.", impact: "Supports 50+ species"},
    {title: "Reduce Plastic Use", category: "Waste", difficulty: "Easy", description: "Use reusable bags, bottles, and containers to minimize plastic waste.", impact: "Prevents 100kg plastic waste per year"},
    {title: "Bike to Work", category: "Lifestyle", difficulty: "Easy", description: "Cycle for short trips instead of driving to reduce emissions.", impact: "Saves 500kg CO₂ per year"}
  ];

  const handleMarkDone = (actionTitle) => {
    setCompletedActions(prev => {
      const newSet = new Set(prev);
      if (newSet.has(actionTitle)) {
        newSet.delete(actionTitle);
      } else {
        newSet.add(actionTitle);
      }
      return newSet;
    });
  };

  const filteredActions = selectedCategory === 'all' 
    ? actions 
    : actions.filter(action => action.category?.toLowerCase() === selectedCategory);

  return (
    <div className="green-actions-container">
      <header className="green-actions-header">
        <div className="hero-content">
          <h1>Take Charge and Make a<br />Difference</h1>
          <p>Small acts create big change. Choose actions that fit<br />your lifestyle and track your environmental impact.</p>
        </div>
      </header>

      <CategoryTabs 
        selectedCategory={selectedCategory}
        onCategoryChange={setSelectedCategory}
      />

      <ActionFeed 
        actions={filteredActions}
        loading={loading}
        completedActions={completedActions}
        onMarkDone={handleMarkDone}
      />
    </div>
  );
};

export default GreenActions;