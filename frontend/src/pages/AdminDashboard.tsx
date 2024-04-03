import React from 'react';
import '../assets/AdminDashboard.css'; // Assuming you have a CSS file for styling

const AdminDashboard: React.FC = () => {
  return (
    <div className="admin-dashboard">
      <div className="admin-buttons">
        <button className="large-button">Add Books</button>
        <button className="large-button">Edit Books</button>
        <button className="large-button">Edit Users</button>
      </div>
      <button className="logout-button">Logout</button>
    </div>
  );
};

export default AdminDashboard;
