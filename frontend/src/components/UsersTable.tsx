import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Checkbox, Button } from '@mui/material';

interface WaitlistBook {
  title: string;
}

interface BorrowedBook {
  title: string;
}

interface UserInfo {
  email: string;
  uid: string;
  waitlistBooks: WaitlistBook[];
  borrowedBooks: BorrowedBook[];
}

const UsersTable: React.FC = () => {
  const [users, setUsers] = useState<UserInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedRows, setSelectedRows] = useState<string[]>([]);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/users');
        console.log('API Response:', response.data);
        if (response.data.success) {
          setUsers(response.data.userInfo);
        } else {
          setError('Failed to fetch user data.');
        }
      } catch (error) {
        console.error('Error fetching users:', error);
        setError('Error fetching user data.');
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  const handleCheckboxChange = (uid: string) => {
    if (selectedRows.includes(uid)) {
      setSelectedRows(selectedRows.filter(id => id !== uid));
    } else {
      setSelectedRows([...selectedRows, uid]);
    }
  };

  const handleDeleteSelectedUsers = async () => {
    try {
      await Promise.all(selectedRows.map(async (uid) => {
        await axios.delete(`http://127.0.0.1:8000/users/${uid}`);
      }));
      // Refresh user list after deletion
      setLoading(true);
      setUsers([]);
      setSelectedRows([]);
      setError(null);
    } catch (error) {
      console.error('Error deleting users:', error);
      setError('Error deleting users.');
    } finally {
      setLoading(false);
    }
  };
  

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <Button variant="contained" color="primary" onClick={handleDeleteSelectedUsers}>
        Delete Selected Users
      </Button>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Email</TableCell>
              <TableCell>Waitlisted Books</TableCell>
              <TableCell>Borrowed Books</TableCell>
              <TableCell>Select</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {users.map((user, index) => (
              <TableRow key={index}>
                <TableCell>{user.email}</TableCell>
                <TableCell>
                  <ul>
                    {user.waitlistBooks && user.waitlistBooks.map((book, bookIndex) => (
                      <li key={`waitlist-${index}-${bookIndex}`}>{book.title}</li>
                    ))}
                  </ul>
                </TableCell>
                <TableCell>
                  <ul>
                    {user.borrowedBooks && user.borrowedBooks.map((book, bookIndex) => (
                      <li key={`borrowed-${index}-${bookIndex}`}>{book.title}</li>
                    ))}
                  </ul>
                </TableCell>
                <TableCell>
                  <Checkbox
                    checked={selectedRows.includes(user.uid)}
                    onChange={() => handleCheckboxChange(user.uid)}
                  />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};

export default UsersTable;