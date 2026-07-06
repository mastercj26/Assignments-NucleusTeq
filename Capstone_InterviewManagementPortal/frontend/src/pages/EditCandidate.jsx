import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { candidateApi } from '../api/candidateApi';
import { jobApi } from '../api/jobApi';
import { getErrorMessage } from '../utils/errorHandler';

const EditCandidate = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [jobs, setJobs] = useState([]);
  const [form, setForm] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch candidate and jobs
        const [candRes, jobsRes] = await Promise.all([
          candidateApi.get(id),
          jobApi.list(1, 100)
        ]);
        setForm(candRes.data);
        setJobs(jobsRes.data.jobs);
      } catch (err) {
        setError(getErrorMessage(err));
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [id]);

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
    setError('');
    setSuccess(false);
    try {
      await candidateApi.update(id, form);
      setSuccess(true);
      setTimeout(() => navigate('/candidates'), 1500);
    } catch (err) {
      setError(getErrorMessage(err));
    }
  };

  if (loading) return <p>Loading candidate...</p>;
  if (error && !form) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <div style={{ maxWidth: '600px', margin: '20px auto' }}>
      <h2>Edit Candidate</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {success && <p style={{ color: 'green' }}>Candidate updated successfully!</p>}
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
          <label>Email</label>
          <input type="email" name="email" value={form.email} onChange={handleChange} required style={{ width: '100%', padding: '8px' }} />
        </div>
        <div style={{ marginTop: '10px' }}>
          <label>Mobile Number</label>
          <input type="tel" name="mobile_number" value={form.mobile_number} onChange={handleChange} required style={{ width: '100%', padding: '8px' }} />
        </div>
        <div style={{ marginTop: '10px' }}>
          <label>Current Company</label>
          <input name="current_company" value={form.current_company || ''} onChange={handleChange} style={{ width: '100%', padding: '8px' }} />
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
        </div>
        <div style={{ marginTop: '10px' }}>
          <label>Status</label>
          <select name="status" value={form.status} onChange={handleChange} style={{ width: '100%', padding: '8px' }}>
            <option value="PROFILE_CREATED">PROFILE_CREATED</option>
            <option value="INTERVIEW_SCHEDULED">INTERVIEW_SCHEDULED</option>
            <option value="INTERVIEW_COMPLETED">INTERVIEW_COMPLETED</option>
            <option value="SELECTED">SELECTED</option>
            <option value="REJECTED">REJECTED</option>
          </select>
        </div>
        <button type="submit" style={{ marginTop: '20px', padding: '10px 20px' }}>
          Update Candidate
        </button>
      </form>
    </div>
  );
};

export default EditCandidate;