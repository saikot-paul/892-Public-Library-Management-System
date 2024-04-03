import React from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate from react-router-dom
import { Button } from '@mui/material';
import UsersTable from '../components/UsersTable';

const EditUsers: React.FC = () => {
  const navigate = useNavigate(); // Use useNavigate hook

  const handleCancel = () => {
    navigate('/admindashboard'); // Use navigate function to redirect
  };

  return (
    <div>
      <h1>Edit Users</h1>
      <UsersTable />
      <div>
        <Button variant="contained" onClick={handleCancel}>
          Cancel
        </Button>
      </div>
    </div>
  );
};

export default EditUsers;
