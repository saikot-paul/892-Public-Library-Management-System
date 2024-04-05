import React from 'react';
import { Link } from 'react-router-dom'; // Import Link from React Router
import '../assets/AdminDashboard.css'; // Assuming you have a CSS file for styling

const AdminDashboard: React.FC = () => {
  const handleLogout = () => {
    localStorage.removeItem('authToken');
    window.location.href = '/';
  };
  return (
    <div className="admin-dashboard">
      <div className="admin-buttons">
        {/* Use Link components for navigation */}
        <Link to="/addbooks" className="large-button">Add Books</Link>
        <Link to="/editbooks" className="large-button">Edit Books</Link>
        <Link to="/editusers" className="large-button">Edit Users</Link>
      </div>
      {/* Logout button with click event handler */}
      <button className="logout-button" onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default AdminDashboard;
