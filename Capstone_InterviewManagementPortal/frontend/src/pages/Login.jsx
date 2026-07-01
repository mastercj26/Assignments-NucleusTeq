import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom'; // <-- import Link
import api from '../api/axiosConfig';
import { getErrorMessage } from '../utils/errorHandler';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    const trimmedEmail = email.trim();
    if (!trimmedEmail || !trimmedEmail.includes('@')) {
      setError('Please enter a valid email address.');
      return;
    }

    try {
      const response = await api.post('/auth/login', { email: trimmedEmail, password });
      const { access_token, user_id, email: userEmail, role } = response.data;
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user_id', user_id);
      localStorage.setItem('user_email', userEmail);
      localStorage.setItem('user_role', role);
      navigate('/dashboard');
    } catch (err) {
      const errorMessage = getErrorMessage(err);
      if (errorMessage.toLowerCase().includes('reset your password')) {
        localStorage.setItem('reset_email', trimmedEmail);
        navigate('/reset-password', { state: { email: trimmedEmail } });
      } else {
        setError(errorMessage);
      }
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '100px auto', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
      <h2>Login</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', margin: '8px 0' }}
          />
        </div>
        <div>
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', margin: '8px 0' }}
          />
        </div>
        <button 
          type="submit" 
          style={{ 
            width: '100%', 
            padding: '10px', 
            background: '#007bff', 
            color: '#fff', 
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Login
        </button>
      </form>

      {/* ====== NEW: Create User Link ====== */}
      <div style={{ marginTop: '20px', textAlign: 'center', borderTop: '1px solid #ddd', paddingTop: '15px' }}>
        <p style={{ margin: 0, fontSize: '14px' }}>
          Don't have an account?{' '}
          <Link 
            to="/users/create" 
            style={{ 
              color: '#28a745', 
              textDecoration: 'underline',
              fontWeight: 'bold'
            }}
          >
            Create User
          </Link>
        </p>
        <p style={{ margin: '5px 0 0', fontSize: '12px', color: '#888' }}>
          (Admin users can create new users from here)
        </p>
      </div>
    </div>
  );
};

export default Login;