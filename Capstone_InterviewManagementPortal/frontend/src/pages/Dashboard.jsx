import React, { useEffect, useState } from 'react';
import api from '../api/axiosConfig';

const Dashboard = () => {
  const [status, setStatus] = useState('Checking...');

  useEffect(() => {
    api.get('/health')
      .then(response => setStatus(response.data.status))
      .catch(error => setStatus('Error: ' + error.message));
  }, []);

  const userEmail = localStorage.getItem('user_email') || 'User';

  return (
    <div>
      <h2>Dashboard</h2>
      <p>Welcome, {userEmail}!</p>
      <p>Backend health: {status}</p>
    </div>
  );
};

export default Dashboard;