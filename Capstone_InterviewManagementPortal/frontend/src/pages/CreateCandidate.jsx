import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { candidateApi } from '../api/candidateApi';
import { jobApi } from '../api/jobApi';
import { getErrorMessage } from '../utils/errorHandler';

const CreateCandidate = () => {
  const navigate = useNavigate();
  const [jobs, setJobs] = useState([]);
  const [form, setForm] = useState({
    first_name: '',
    last_name: '',
    email: '',
    mobile_number: '',
    current_company: '',
    total_experience: 0,
    applied_job_id: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Fetch jobs for dropdown
    const fetchJobs = async () => {
      try {
        const res = await jobApi.list(1, 100); // get all jobs
        setJobs(res.data.jobs);
        if (res.data.jobs.length > 0) {
          setForm(prev => ({ ...prev, applied_job_id: res.data.jobs[0].id }));
        }
      } catch (err) {
        setError('Could not load jobs. Please try again.');
      }
    };
    fetchJobs();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const validate = () => {
    if (!form.applied_job_id) {
      setError('Please select a job.');
      return false;
    }
    if (!form.email.endsWith('@nucleusteq.com')) {
      setError('Email must be from nucleusteq.com domain');
      return false;
    }
    if (!/^[0-9]{10}$/.test(form.mobile_number)) {
      setError('Mobile number must be exactly 10 digits');
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
      await candidateApi.create(form);
      navigate('/candidates');
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '20px auto' }}>
      <h2>Add New Candidate</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>First Name</label>
          <input name="first_name" value={form.first_name} onChange={handleChange} required style={{ width: '100%', padding: '8px' }} />
        </div>
        <div style={{ marginTop: '10px' }}>
          <label>Last Name</label>
          <input name="last_name" value={form.last_name} onChange={handleChange} required style={{ width: '100%', padding: '8px' }} />
        </div>
        <div style={{ marginTop: '10px' }}>
          <label>Email (must end with @nucleusteq.com)</label>
          <input type="email" name="email" value={form.email} onChange={handleChange} required style={{ width: '100%', padding: '8px' }} />
        </div>
        <div style={{ marginTop: '10px' }}>
          <label>Mobile Number (10 digits)</label>
          <input type="tel" name="mobile_number" value={form.mobile_number} onChange={handleChange} required style={{ width: '100%', padding: '8px' }} />
        </div>
        <div style={{ marginTop: '10px' }}>
          <label>Current Company (optional)</label>
          <input name="current_company" value={form.current_company} onChange={handleChange} style={{ width: '100%', padding: '8px' }} />
        </div>
        <div style={{ marginTop: '10px' }}>
          <label>Total Experience (years)</label>
          <input type="number" name="total_experience" value={form.total_experience} onChange={handleChange} min="0" step="0.5" required style={{ width: '100%', padding: '8px' }} />
        </div>
        <div style={{ marginTop: '10px' }}>
          <label>Applied Job</label>
          <select name="applied_job_id" value={form.applied_job_id} onChange={handleChange} required style={{ width: '100%', padding: '8px' }}>
            {jobs.map(job => (
              <option key={job.id} value={job.id}>{job.job_title}</option>
            ))}
          </select>
          {jobs.length === 0 && <small style={{ color: 'red' }}>No jobs found. Please create a job first.</small>}
        </div>
        <button type="submit" disabled={loading} style={{ marginTop: '20px', padding: '10px 20px' }}>
          {loading ? 'Creating...' : 'Create Candidate'}
        </button>
      </form>
    </div>
  );
};

export default CreateCandidate;