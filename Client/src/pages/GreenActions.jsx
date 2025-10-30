import React, { useState, useEffect } from "react";
import "../styles/GreenActions.css";
import ActionFeed from "../components/ActionFeed";
import CategoryTabs from "../components/CategoryTabs";
import { API_BASE_URL } from "../services/api";

const GreenActions = () => {
  const [actions, setActions] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [loading, setLoading] = useState(true);
  const [completedActions, setCompletedActions] = useState(new Set());
  const [currentTask, setCurrentTask] = useState(null);
  const [taskCompleted, setTaskCompleted] = useState(false);
  const [completedTasks, setCompletedTasks] = useState([]);

  useEffect(() => {
    fetchGreenActions();
    generateNewTask();
  }, []);

  const fetchGreenActions = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/ai/green-advice`);
      if (response.ok) {
        const data = await response.json();
        setActions(data.actions);
      } else {
        setActions([]);
      }
    } catch (error) {
      setActions([]);
    } finally {
      setLoading(false);
    }
  };

  const generateNewTask = async () => {
    try {
      const response = await fetch(
        `${API_BASE_URL}/ai/generate-task`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            category: selectedCategory === "all" ? "general" : selectedCategory,
            difficulty: null,
            location: null,
          }),
        }
      );

      if (response.ok) {
        const data = await response.json();
        setCurrentTask(data.task);
        setTaskCompleted(false);
      }
    } catch (error) {
      console.error("Failed to generate task:", error);
    }
  };

  const handleTaskComplete = () => {
    if (currentTask) {
      setCompletedTasks((prev) => [...prev, currentTask]);
    }
    setTaskCompleted(true);
    setTimeout(() => {
      generateNewTask();
    }, 2000);
  };

  const mockActions = [
    {
      title: "Switch to LED Bulbs",
      category: "Energy",
      difficulty: "Easy",
      description:
        "Replace traditional bulbs with energy efficient LED lights throughout your home.",
      impact: "Saves 75% energy, reduces 200kg CO₂/year",
    },
    {
      title: "Collect Rainwater",
      category: "Water",
      difficulty: "Medium",
      description:
        "Set up rainwater harvesting system for watering plants and gardens.",
      impact: "Saves 500+ litres per month",
    },
    {
      title: "Plant Native Trees",
      category: "Nature",
      difficulty: "Medium",
      description:
        "Plant indigenous tree species in your community to restore ecosystem.",
      impact: "Absorb 20kg carbon dioxide per tree",
    },
    {
      title: "Start Composting",
      category: "Waste",
      difficulty: "Medium",
      description: "Turn food waste into nutrient-rich compost for gardening.",
      impact: "Diverts 150kg waste from landfills per year",
    },
    {
      title: "Install Solar Panels",
      category: "Energy",
      difficulty: "Hard",
      description:
        "Generate clean energy by installing solar panels on your roof.",
      impact: "Saves 3,000kgs carbon dioxide per year",
    },
    {
      title: "Fix Water Leaks",
      category: "Water",
      difficulty: "Easy",
      description: "Repair dripping taps and leaking pipes to conserve water.",
      impact: "Saves 20 litres per day",
    },
    {
      title: "Use Public Transport",
      category: "Lifestyle",
      difficulty: "Easy",
      description: "Choose buses, trains, or carpool instead of driving alone.",
      impact: "Reduces 1,000kg carbon dioxide per year",
    },
    {
      title: "Create Wildlife Habitat",
      category: "Nature",
      difficulty: "Medium",
      description:
        "Plant native flowers and shrubs to support local pollinators and birds.",
      impact: "Supports 50+ species",
    },
    {
      title: "Reduce Plastic Use",
      category: "Waste",
      difficulty: "Easy",
      description:
        "Use reusable bags, bottles, and containers to minimize plastic waste.",
      impact: "Prevents 100kg plastic waste per year",
    },
    {
      title: "Bike to Work",
      category: "Lifestyle",
      difficulty: "Easy",
      description:
        "Cycle for short trips instead of driving to reduce emissions.",
      impact: "Saves 500kg CO₂ per year",
    },
  ];

  const handleMarkDone = (actionTitle) => {
    setCompletedActions((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(actionTitle)) {
        newSet.delete(actionTitle);
      } else {
        newSet.add(actionTitle);
      }
      return newSet;
    });
  };

  const filteredActions =
    selectedCategory === "all"
      ? actions
      : actions.filter(
          (action) => action.category?.toLowerCase() === selectedCategory
        );

  return (
    <div className="green-actions-container">
      <header className="green-actions-header">
        <div className="hero-content">
          <div className="hero-image-container">
            <div className="hero-text-overlay">
              <h1>
                Take Charge and Make a<br />
                Difference
              </h1>
              <p>
                Small acts create big change. Choose actions that fit your
                lifestyle and track your environmental impact.
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Completed Tasks Section */}
      {completedTasks.length > 0 && (
        <div className="completed-tasks-section">
          <h2>✅ Completed Tasks</h2>
          <div className="completed-tasks-list">
            {completedTasks.map((task, index) => (
              <div key={index} className="completed-task-card">
                <div className="task-header">
                  <h3>{task.title}</h3>
                  <div className="task-meta">
                    <span className="task-category">{task.category}</span>
                    <span
                      className={`task-difficulty ${task.difficulty.toLowerCase()}`}
                    >
                      {task.difficulty}
                    </span>
                  </div>
                </div>
                <p className="task-description">{task.description}</p>
                <div className="task-details">
                  <p className="task-impact">
                    <strong>Impact:</strong> {task.impact}
                  </p>
                  <p className="task-time">
                    <strong>Time:</strong> {task.time_estimate}
                  </p>
                  {task.materials_needed &&
                    task.materials_needed.length > 0 && (
                      <p className="task-materials">
                        <strong>Materials:</strong>{" "}
                        {task.materials_needed.join(", ")}
                      </p>
                    )}
                </div>
                <div className="task-completed">
                  <span className="checkmark">✓</span>
                  <span>Completed</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* AI-Generated Task Section */}
      {currentTask && (
        <div className="current-task-section">
          <h2>🌱 Your Daily Green Task</h2>
          <div className={`task-card ${taskCompleted ? "completed" : ""}`}>
            <div className="task-header">
              <h3>{currentTask.title}</h3>
              <div className="task-meta">
                <span className="task-category">{currentTask.category}</span>
                <span
                  className={`task-difficulty ${currentTask.difficulty.toLowerCase()}`}
                >
                  {currentTask.difficulty}
                </span>
              </div>
            </div>
            <p className="task-description">{currentTask.description}</p>
            <div className="task-details">
              <p className="task-impact">
                <strong>Impact:</strong> {currentTask.impact}
              </p>
              <p className="task-time">
                <strong>Time:</strong> {currentTask.time_estimate}
              </p>
              {currentTask.materials_needed &&
                currentTask.materials_needed.length > 0 && (
                  <p className="task-materials">
                    <strong>Materials:</strong>{" "}
                    {currentTask.materials_needed.join(", ")}
                  </p>
                )}
            </div>
            {!taskCompleted ? (
              <button
                className="complete-task-btn"
                onClick={handleTaskComplete}
              >
                Mark Task Complete
              </button>
            ) : (
              <div className="task-completed">
                <span className="checkmark">✓</span>
                <span>Task Completed! Great job!</span>
              </div>
            )}
          </div>
          <button className="new-task-btn" onClick={generateNewTask}>
            Generate New Task
          </button>
        </div>
      )}

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
