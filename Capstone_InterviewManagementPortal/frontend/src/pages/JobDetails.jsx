import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { jobApi } from '../api/jobApi';
import { getErrorMessage } from '../utils/errorHandler';

const JobDetails = () => {
  const { id } = useParams();
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchJob = async () => {
      try {
        const res = await jobApi.get(id);
        setJob(res.data);
      } catch (err) {
        setError(getErrorMessage(err));
      } finally {
        setLoading(false);
      }
    };
    fetchJob();
  }, [id]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;
  if (!job) return <p>Job not found</p>;

  return (
    <div>
      <h2>{job.job_title}</h2>
      <p><strong>Role:</strong> {job.job_role}</p>
      <p><strong>Details:</strong> {job.job_details}</p>
      <p><strong>Experience:</strong> {job.experience_required} years</p>
      <p><strong>Employment:</strong> {job.employment_type}</p>
      <p><strong>Location:</strong> {job.location}</p>
      <p><strong>Status:</strong> {job.status}</p>
      <p><strong>Skills:</strong> {job.required_skills.join(', ')}</p>
    </div>
  );
};

export default JobDetails;