import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { jobApi } from '../api/jobApi';
import { getErrorMessage } from '../utils/errorHandler';

const CreateJob = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    job_title: '',
    job_details: '',
    job_role: '',
    required_skills: [],
    experience_required: 0,
    employment_type: 'Full Time',
    location: '',
    status: 'open'
  });
  const [skillsInput, setSkillsInput] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const employmentTypes = ['Full Time', 'Internship'];
  const statuses = ['open', 'closed', 'draft'];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const addSkill = () => {
    if (skillsInput.trim() && !form.required_skills.includes(skillsInput.trim())) {
      setForm({ ...form, required_skills: [...form.required_skills, skillsInput.trim()] });
      setSkillsInput('');
    }
  };

  const removeSkill = (skill) => {
    setForm({ ...form, required_skills: form.required_skills.filter(s => s !== skill) });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (form.required_skills.length === 0) {
      setError('At least one skill is required.');
      return;
    }
    setLoading(true);
    setError('');
    try {
      await jobApi.create(form);
      navigate('/jobs');
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '20px auto' }}>
      <h2>Create Job Description</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Job Title</label>
          <input name="job_title" value={form.job_title} onChange={handleChange} required style={{ width: '100%', padding: '8px' }} />
        </div>
        <div style={{ marginTop: '10px' }}>
          <label>Job Details</label>
          <textarea name="job_details" value={form.job_details} onChange={handleChange} required rows="4" style={{ width: '100%', padding: '8px' }} />
        </div>
        <div style={{ marginTop: '10px' }}>
          <label>Job Role</label>
          <input name="job_role" value={form.job_role} onChange={handleChange} required style={{ width: '100%', padding: '8px' }} />
        </div>
        <div style={{ marginTop: '10px' }}>
          <label>Required Skills</label>
          <div style={{ display: 'flex' }}>
            <input
              type="text"
              value={skillsInput}
              onChange={(e) => setSkillsInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addSkill())}
              style={{ flex: 1, padding: '8px' }}
              placeholder="Type skill and press Enter"
            />
            <button type="button" onClick={addSkill} style={{ padding: '8px 16px' }}>Add</button>
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '8px' }}>
            {form.required_skills.map(skill => (
              <span key={skill} style={{ background: '#e0e0e0', padding: '4px 10px', borderRadius: '4px', display: 'flex', alignItems: 'center' }}>
                {skill}
                <button type="button" onClick={() => removeSkill(skill)} style={{ marginLeft: '8px', background: 'transparent', border: 'none', cursor: 'pointer' }}>✕</button>
              </span>
            ))}
          </div>
        </div>
        <div style={{ marginTop: '10px' }}>
          <label>Experience Required (years)</label>
          <input name="experience_required" type="number" value={form.experience_required} onChange={handleChange} min="0" style={{ width: '100%', padding: '8px' }} />
        </div>
        <div style={{ marginTop: '10px' }}>
          <label>Employment Type</label>
          <select name="employment_type" value={form.employment_type} onChange={handleChange} style={{ width: '100%', padding: '8px' }}>
            {employmentTypes.map(type => (
              <option key={type} value={type}>{type}</option>
            ))}
          </select>
        </div>
        <div style={{ marginTop: '10px' }}>
          <label>Location</label>
          <input name="location" value={form.location} onChange={handleChange} required style={{ width: '100%', padding: '8px' }} />
        </div>
        <div style={{ marginTop: '10px' }}>
          <label>Status</label>
          <select name="status" value={form.status} onChange={handleChange} style={{ width: '100%', padding: '8px' }}>
            {statuses.map(s => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>
        <button type="submit" disabled={loading} style={{ marginTop: '20px', padding: '10px 20px' }}>
          {loading ? 'Creating...' : 'Create Job'}
        </button>
      </form>
    </div>
  );
};

export default CreateJob;