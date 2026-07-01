import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { userApi } from '../api/userApi';
import { getErrorMessage } from '../utils/errorHandler';

const EditUser = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    first_name: '',
    last_name: '',
    role: '',
    status: ''
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await userApi.get(id);
        setForm({
          first_name: res.data.first_name || '',
          last_name: res.data.last_name || '',
          role: res.data.role || '',
          status: res.data.status || ''
        });
      } catch (err) {
        setError(getErrorMessage(err));
      } finally {
        setLoading(false);
      }
    };
    fetchUser();
  }, [id]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess(false);
    try {
      await userApi.update(id, form);
      setSuccess(true);
      setTimeout(() => navigate('/users'), 1500);
    } catch (err) {
      setError(getErrorMessage(err));
    }
  };

  if (loading) return <p>Loading user...</p>;
  if (error && !form.first_name) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <div style={{ maxWidth: '500px', margin: '20px auto' }}>
      <h2>Edit User</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {success && <p style={{ color: 'green' }}>User updated successfully!</p>}
      <form onSubmit={handleSubmit}>
        <div>
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
            <option value="admin">admin</option>
            <option value="hr">hr</option>
            <option value="interviewer">interviewer</option>
          </select>
        </div>
        <div style={{ marginTop: '10px' }}>
          <label>Status</label>
          <select
            name="status"
            value={form.status}
            onChange={handleChange}
            style={{ width: '100%', padding: '8px' }}
          >
            <option value="active">active</option>
            <option value="inactive">inactive</option>
          </select>
        </div>
        <button
          type="submit"
          style={{ marginTop: '20px', padding: '10px 20px' }}
        >
          Update User
        </button>
      </form>
    </div>
  );
};

export default EditUser;