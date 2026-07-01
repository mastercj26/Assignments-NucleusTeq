import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { userApi } from '../api/userApi';
import { getErrorMessage } from '../utils/errorHandler';

const Users = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const fetchUsers = async (pageNum = 1) => {
    setLoading(true);
    setError('');
    try {
      const res = await userApi.list(pageNum);
      setUsers(res.data.users);
      setTotalPages(res.data.pages);
      setPage(res.data.page);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers(page);
  }, [page]);

  const handleToggleStatus = async (id, currentActive) => {
    if (!window.confirm(`Are you sure you want to ${currentActive ? 'disable' : 'enable'} this user?`)) return;
    try {
      await userApi.toggleStatus(id, !currentActive);
      // Refresh list
      fetchUsers(page);
    } catch (err) {
      alert(getErrorMessage(err));
    }
  };

  if (loading) return <p>Loading users...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <div>
      <h2>User Management</h2>
      <Link to="/users/create">
        <button style={{ marginBottom: '20px' }}>Create New User</button>
      </Link>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ background: '#f4f4f4' }}>
            <th>Email</th>
            <th>Name</th>
            <th>Role</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id} style={{ borderBottom: '1px solid #ddd' }}>
              <td>{user.email}</td>
              <td>{user.first_name} {user.last_name}</td>
              <td>{user.role}</td>
              <td>{user.status}</td>
              <td>
                <Link to={`/users/edit/${user.id}`}>
                  <button>Edit</button>
                </Link>
                <button 
                  onClick={() => handleToggleStatus(user.id, user.status === 'active')}
                  style={{ 
                    background: user.status === 'active' ? '#dc3545' : '#28a745',
                    marginLeft: '10px'
                  }}
                >
                  {user.status === 'active' ? 'Disable' : 'Enable'}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {/* Pagination */}
      <div style={{ marginTop: '20px' }}>
        <button disabled={page <= 1} onClick={() => setPage(p => p - 1)}>Previous</button>
        <span style={{ margin: '0 15px' }}>Page {page} of {totalPages}</span>
        <button disabled={page >= totalPages} onClick={() => setPage(p => p + 1)}>Next</button>
      </div>
    </div>
  );
};

export default Users;