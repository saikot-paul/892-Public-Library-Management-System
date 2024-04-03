import React, { useState, useEffect } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

interface Book {
  title: string;
  author: string;
  genre: string;
  isbn: string;
  bookId: number;
  status: boolean;
}

const BooksTable: React.FC = () => {
  const [books, setBooks] = useState<Book[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetch('http://127.0.0.1:5000/books/get_all')
      .then(response => response.json())
      .then(data => {
        console.log(data); // Check what data is fetched
        setBooks(data.books);
      })
      .catch(error => {
        console.error('Error fetching books:', error);
      });
  }, []);

  const handleCancel = () => {
    navigate('/admindashboard');
  };

  const handleDelete = async (bookId: number) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/books/get/${bookId}`);
      const data = await response.json();
      const bookStatus = data.status;

      if (bookStatus === false) {
        await fetch(`http://127.0.0.1:5000/books/delete_book/${bookId}`, {
          method: 'DELETE',
        });
        // Refresh books after deletion
        setBooks(books.filter(book => book.bookId !== bookId));
      } else {
        alert('Cannot delete book. Book status is true.');
      }
    } catch (error) {
      console.error('Error deleting book:', error);
    }
  };

  return (
    <div>
      <h2>Books</h2>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Title</TableCell>
              <TableCell>Author</TableCell>
              <TableCell>Genre</TableCell>
              <TableCell>ISBN</TableCell>
              <TableCell>Book ID</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {books && books.map(book => (
              <TableRow key={book.bookId}>
                <TableCell>{book.title}</TableCell>
                <TableCell>{book.author}</TableCell>
                <TableCell>{book.genre}</TableCell>
                <TableCell>{book.isbn}</TableCell>
                <TableCell>{book.bookId}</TableCell>
                <TableCell>
                  <Button onClick={() => handleDelete(book.bookId)}>Delete</Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <Button onClick={handleCancel}>Cancel</Button>
    </div>
  );
};

export default BooksTable;
