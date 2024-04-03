import React, { useState } from "react";

interface Book {
  id: number;
  title: string;
  isbn: string;
  author: string;
  genre: string;
  copies: number;
  cover: string;
}

const EditBooks: React.FC = () => {
  const initialBooks: Book[] = [
    {
      id: 1,
      title: "Book 1",
      isbn: "123456789",
      author: "Author 1",
      genre: "Fiction",
      copies: 5,
      cover: "book1.jpg",
    },
    {
      id: 2,
      title: "Book 2",
      isbn: "987654321",
      author: "Author 2",
      genre: "Non-Fiction",
      copies: 3,
      cover: "book2.jpg",
    },
    // Add more books as needed
  ];

  const [books, setBooks] = useState<Book[]>(initialBooks);

  const handleCancelClick = () => {
    // Logic to navigate back to AdminDashboard
    console.log("Cancel clicked");
  };

  const handleSaveClick = () => {
    // Logic to save changes to books
    console.log("Save clicked");
  };

  const handleDeleteClick = (id: number) => {
    // Logic to delete a book by id
    console.log("Delete clicked for book with id:", id);
    const updatedBooks = books.filter((book) => book.id !== id);
    setBooks(updatedBooks);
  };

  return (
    <div>
      <h1>Edit Books</h1>
      <div className="books-list">
        <table>
          <thead>
            <tr>
              <th></th>
              <th>Book Title</th>
              <th>ISBN</th>
              <th>Author</th>
              <th>Genre</th>
              <th>Copies</th>
              <th>Cover</th>
            </tr>
          </thead>
          <tbody>
            {books.map((book) => (
              <tr key={book.id}>
                <td><input type="checkbox" /></td>
                <td>{book.title}</td>
                <td>{book.isbn}</td>
                <td>{book.author}</td>
                <td>{book.genre}</td>
                <td>{book.copies}</td>
                <td>{book.cover}</td>
                <td>
                  <button onClick={() => handleDeleteClick(book.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="action-buttons">
        <button onClick={handleCancelClick}>Cancel</button>
        <button onClick={handleSaveClick}>Save</button>
      </div>
    </div>
  );
};

export default EditBooks;
