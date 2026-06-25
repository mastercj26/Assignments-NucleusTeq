import React from 'react';

const Header = () => {
  return (
    <header style={{ padding: '10px 20px', background: '#007bff', color: '#fff' }}>
      <h2>Interview Management</h2>
    </header>
  );
};
const handleLogout = () => {
  localStorage.clear();
  window.location.href = '/login';
};


<button onClick={handleLogout} style={{ float: 'right' }}>Logout</button>
export default Header;