import React from 'react';
import AddBookForm from '../components/AddBookForm'; // Import the BooksTable component

const AddBooks: React.FC = () => {
  return (
    <div>
      <h1>Add Books</h1>
      <AddBookForm /> {/* Display the BooksTable component */}
    </div>
  );
};

export default AddBooks;
