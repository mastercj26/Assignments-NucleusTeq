import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { jobApi } from '../api/jobApi';
import { getErrorMessage } from '../utils/errorHandler';

const Jobs = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const userRole = localStorage.getItem('user_role');
  const canManage = userRole === 'admin' || userRole === 'hr';

  const fetchJobs = async (pageNum = 1) => {
    setLoading(true);
    setError('');
    try {
      const res = await jobApi.list(pageNum);
      setJobs(res.data.jobs);
      setTotalPages(res.data.pages);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchJobs(page);
  }, [page]);

  if (loading) return <p>Loading jobs...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <div>
      <h2>Job Descriptions</h2>
      {canManage && (
        <Link to="/jobs/create">
          <button style={{ marginBottom: '20px' }}>Create New Job</button>
        </Link>
      )}
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ background: '#f4f4f4' }}>
            <th>Title</th>
            <th>Role</th>
            <th>Employment</th>
            <th>Location</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {jobs.map(job => (
            <tr key={job.id} style={{ borderBottom: '1px solid #ddd' }}>
              <td>{job.job_title}</td>
              <td>{job.job_role}</td>
              <td>{job.employment_type}</td>
              <td>{job.location}</td>
              <td>{job.status}</td>
              <td>
                <Link to={`/jobs/${job.id}`}>
                  <button>View</button>
                </Link>
                {canManage && (
                  <Link to={`/jobs/edit/${job.id}`} style={{ marginLeft: '10px' }}>
                    <button>Edit</button>
                  </Link>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <div style={{ marginTop: '20px' }}>
        <button disabled={page <= 1} onClick={() => setPage(p => p - 1)}>Previous</button>
        <span style={{ margin: '0 15px' }}>Page {page} of {totalPages}</span>
        <button disabled={page >= totalPages} onClick={() => setPage(p => p + 1)}>Next</button>
      </div>
    </div>
  );
};

export default Jobs;