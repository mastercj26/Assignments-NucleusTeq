import React from 'react';
import { Link } from 'react-router-dom';

const Sidebar = () => {
  return (
    <div style={{ width: '200px', background: '#f4f4f4', padding: '20px', height: '100vh' }}>
      <h3>Interview Portal</h3>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        <li><Link to="/dashboard">Dashboard</Link></li>
        <li><Link to="/jobs">Jobs</Link></li>
        <li><Link to="/candidates">Candidates</Link></li>
        <li><Link to="/interviews">Interviews</Link></li>
        <li><Link to="/users">Users</Link></li>
        <li><Link to="/login">Login</Link></li>
        <li><Link to="/change-password">Change Password</Link></li>
      </ul>
    </div>
  );
};

export default Sidebar;