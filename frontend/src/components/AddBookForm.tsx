import React, { useState } from 'react';
import { Button, TextField } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const AddBookForm: React.FC = () => {
  const [formData, setFormData] = useState({
    title: '',
    author: '',
    genre: '',
    isbn: ''
  });

  const navigate = useNavigate();

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSave = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/books/create_book', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          Title: formData.title,
          Author: formData.author,
          Genre: formData.genre,
          ISBN: formData.isbn
        })
      });
      if (response.ok) {
        // Clear form data after successful save
        setFormData({ title: '', author: '', genre: '', isbn: '' });
      } else {
        console.error('Failed to add book');
      }
    } catch (error) {
      console.error('Error adding book:', error);
    }
  };
  
  
  
  

  const handleCancel = () => {
    navigate('/admindashboard');
  };

  return (
    <div>
      <TextField
        label="Title"
        name="title"
        value={formData.title}
        onChange={handleChange}
        fullWidth
        required
      />
      <TextField
        label="Author"
        name="author"
        value={formData.author}
        onChange={handleChange}
        fullWidth
        required
      />
      <TextField
        label="Genre"
        name="genre"
        value={formData.genre}
        onChange={handleChange}
        fullWidth
        required
      />
      <TextField
        label="ISBN"
        name="isbn"
        value={formData.isbn}
        onChange={handleChange}
        fullWidth
        required
      />
      <Button variant="contained" color="primary" onClick={handleSave}>
        Save
      </Button>
      <Button variant="contained" onClick={handleCancel}>
        Cancel
      </Button>
    </div>
  );
};

export default AddBookForm;
