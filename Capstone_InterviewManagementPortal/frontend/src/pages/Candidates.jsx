import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { candidateApi } from '../api/candidateApi';
import { getErrorMessage } from '../utils/errorHandler';
import { CANDIDATE_STATUS_COLORS } from '../constants/candidateConstants';
const Candidates = () => {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const userRole = localStorage.getItem('user_role');
  const canManage = userRole === 'admin' || userRole === 'hr';

  const fetchCandidates = async (pageNum = 1) => {
    setLoading(true);
    setError('');
    try {
      const res = await candidateApi.list(pageNum);
      setCandidates(res.data.candidates);
      setTotalPages(res.data.pages);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCandidates(page);
  }, [page]);

  

  if (loading) return <p>Loading candidates...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <div>
      <h2>Candidate Management</h2>
      {canManage && (
        <Link to="/candidates/create">
          <button style={{ marginBottom: '20px' }}>Add New Candidate</button>
        </Link>
      )}
      {candidates.length === 0 ? (
        <p>No candidates found. Create one!</p>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ background: '#f4f4f4' }}>
              <th>Name</th>
              <th>Email</th>
              <th>Mobile</th>
              <th>Experience</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {candidates.map(c => (
              <tr key={c.id} style={{ borderBottom: '1px solid #ddd' }}>
                <td>{c.first_name} {c.last_name}</td>
                <td>{c.email}</td>
                <td>{c.mobile_number}</td>
                <td>{c.total_experience} yrs</td>
                <td>
                  <span style={{
                    background: CANDIDATE_STATUS_COLORS[c.status] || '#6c757d',
                      color: '#fff',
                     padding: '4px 8px',
                      borderRadius: '4px',
                      fontSize: '12px'  }}>
                                {c.status}
                               </span>
                </td>
                <td>
                  <Link to={`/candidates/${c.id}`}>
                    <button>View</button>
                  </Link>
                  {canManage && (
                    <>
                      <Link to={`/candidates/edit/${c.id}`} style={{ marginLeft: '10px' }}>
                        <button>Edit</button>
                      </Link>
                    </>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      <div style={{ marginTop: '20px' }}>
        <button disabled={page <= 1} onClick={() => setPage(p => p - 1)}>Previous</button>
        <span style={{ margin: '0 15px' }}>Page {page} of {totalPages}</span>
        <button disabled={page >= totalPages} onClick={() => setPage(p => p + 1)}>Next</button>
      </div>
    </div>
  );
};

export default Candidates;