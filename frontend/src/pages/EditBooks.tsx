import React from 'react';
import BooksTable from '../components/BooksTable'; // Import the BooksTable component

const EditBooks: React.FC = () => {
  return (
    <div>
      <h1>Edit Books</h1>
      <BooksTable /> {/* Display the BooksTable component */}
    </div>
  );
};

export default EditBooks;
