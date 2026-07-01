import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { userApi } from '../api/userApi';
import { getErrorMessage } from '../utils/errorHandler';

const CreateUser = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    role: 'hr' // default role
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const roles = ['admin', 'hr', 'interviewer'];

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const validate = () => {
    if (!form.email.endsWith('@nucleusteq.com')) {
      setError('Email must be from nucleusteq.com domain');
      return false;
    }
    if (form.password.length < 6 || form.password.length > 12) {
      setError('Password must be 6-12 characters');
      return false;
    }
    if (!/^[A-Za-z0-9@#$%^&+=!]{6,12}$/.test(form.password)) {
      setError('Password must contain alphanumeric or special characters (@#$%^&+=!)');
      return false;
    }
    if (!form.first_name.trim() || !form.last_name.trim()) {
      setError('First and last name are required');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;
    setLoading(true);
    setError('');
    try {
      await userApi.create(form);
      navigate('/users');
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '500px', margin: '20px auto' }}>
      <h2>Create New User</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email (must end with @nucleusteq.com)</label>
          <input
            type="email"
            name="email"
            value={form.email}
            onChange={handleChange}
            required
            style={{ width: '100%', padding: '8px' }}
          />
        </div>
        <div style={{ marginTop: '10px' }}>
          <label>Password (6-12 chars)</label>
          <input
            type="password"
            name="password"
            value={form.password}
            onChange={handleChange}
            required
            style={{ width: '100%', padding: '8px' }}
          />
        </div>
        <div style={{ marginTop: '10px' }}>
          <label>First Name</label>
          <input
            type="text"
            name="first_name"
            value={form.first_name}
            onChange={handleChange}
            required
            style={{ width: '100%', padding: '8px' }}
          />
        </div>
        <div style={{ marginTop: '10px' }}>
          <label>Last Name</label>
          <input
            type="text"
            name="last_name"
            value={form.last_name}
            onChange={handleChange}
            required
            style={{ width: '100%', padding: '8px' }}
          />
        </div>
        <div style={{ marginTop: '10px' }}>
          <label>Role</label>
          <select
            name="role"
            value={form.role}
            onChange={handleChange}
            style={{ width: '100%', padding: '8px' }}
          >
            {roles.map(r => (
              <option key={r} value={r}>{r}</option>
            ))}
          </select>
        </div>
        <button
          type="submit"
          disabled={loading}
          style={{ marginTop: '20px', padding: '10px 20px' }}
        >
          {loading ? 'Creating...' : 'Create User'}
        </button>
      </form>
    </div>
  );
};

export default CreateUser;