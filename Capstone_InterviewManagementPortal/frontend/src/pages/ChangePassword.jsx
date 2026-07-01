import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axiosConfig';
import { getErrorMessage } from '../utils/errorHandler';

const ChangePassword = () => {
  const navigate = useNavigate();
  const email = localStorage.getItem('user_email') || ''; // already logged in

  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate new password
    if (newPassword.length < 6 || newPassword.length > 12) {
      setError('New password must be 6–12 characters long.');
      return;
    }
    if (!/^[A-Za-z0-9@#$%^&+=!]{6,12}$/.test(newPassword)) {
      setError('Password must contain only letters, numbers, or special characters (@#$%^&+=!).');
      return;
    }
    if (newPassword !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setError('');
    setMessage('');

    try {
      await api.post('/auth/reset-password', {
        email,
        old_password: oldPassword,
        new_password: newPassword,
      });
      setMessage('Password changed successfully!');
      setTimeout(() => navigate('/dashboard'), 2000);
    } catch (err) {
      const errorMsg = getErrorMessage(err);
      setError(errorMsg);
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto', padding: '20px', border: '1px solid #ccc' }}>
      <h2>Change Password</h2>
      {message && <p style={{ color: 'green' }}>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Current Password</label>
          <input
            type="password"
            value={oldPassword}
            onChange={(e) => setOldPassword(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', margin: '8px 0' }}
          />
        </div>
        <div>
          <label>New Password</label>
          <input
            type="password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', margin: '8px 0' }}
          />
        </div>
        <div>
          <label>Confirm New Password</label>
          <input
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', margin: '8px 0' }}
          />
        </div>
        <button
          type="submit"
          style={{
            padding: '10px 20px',
            background: '#28a745',
            color: '#fff',
            border: 'none',
            cursor: 'pointer'
          }}
        >
          Change Password
        </button>
      </form>
    </div>
  );
};

export default ChangePassword;