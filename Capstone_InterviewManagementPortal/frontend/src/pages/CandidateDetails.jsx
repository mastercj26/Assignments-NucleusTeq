import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { candidateApi } from '../api/candidateApi';
import { getErrorMessage } from '../utils/errorHandler';

const CandidateDetails = () => {
  const { id } = useParams();
  const [candidate, setCandidate] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchCandidate = async () => {
      try {
        const res = await candidateApi.get(id);
        setCandidate(res.data);
      } catch (err) {
        setError(getErrorMessage(err));
      } finally {
        setLoading(false);
      }
    };
    fetchCandidate();
  }, [id]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;
  if (!candidate) return <p>Candidate not found</p>;

  return (
    <div>
      <h2>Candidate Details</h2>
      <p><strong>Name:</strong> {candidate.first_name} {candidate.last_name}</p>
      <p><strong>Email:</strong> {candidate.email}</p>
      <p><strong>Mobile:</strong> {candidate.mobile_number}</p>
      <p><strong>Current Company:</strong> {candidate.current_company || 'N/A'}</p>
      <p><strong>Total Experience:</strong> {candidate.total_experience} years</p>
      <p><strong>Applied Job ID:</strong> {candidate.applied_job_id}</p>
      <p><strong>Status:</strong> {candidate.status}</p>
    </div>
  );
};

export default CandidateDetails;