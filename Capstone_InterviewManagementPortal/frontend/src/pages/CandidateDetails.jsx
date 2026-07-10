import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { candidateApi } from '../api/candidateApi';
import { getErrorMessage } from '../utils/errorHandler';
import { CANDIDATE_STATUSES } from '../constants/candidateConstants';  

const CandidateDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [candidate, setCandidate] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const [newStatus, setNewStatus] = useState('');
  const [statusNotes, setStatusNotes] = useState('');
  const [updatingStatus, setUpdatingStatus] = useState(false);

  
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const userRole = localStorage.getItem('user_role');
  const canManage = userRole === 'admin' || userRole === 'hr';

  const fetchData = async () => {
    setLoading(true);
    setError('');
    try {
      const [candRes, histRes] = await Promise.all([
        candidateApi.get(id),
        candidateApi.getStatusHistory(id),
      ]);
      setCandidate(candRes.data);
      setNewStatus(candRes.data.status);
      setHistory(histRes.data.history || []);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [id]);

  const handleStatusUpdate = async (e) => {
    e.preventDefault();
    if (!newStatus) return;
    setUpdatingStatus(true);
    setError('');
    setSuccess('');
    try {
      await candidateApi.updateStatus(id, newStatus, statusNotes);
      setSuccess('Status updated successfully!');
      await fetchData();
      setStatusNotes('');
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setUpdatingStatus(false);
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
    } else {
      setSelectedFile(null);
      alert('Please select a PDF file.');
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    setUploading(true);
    setError('');
    setSuccess('');
    try {
      await candidateApi.uploadResume(id, selectedFile);
      setSuccess('Resume uploaded successfully!');
      setSelectedFile(null);
      await fetchData();
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setUploading(false);
    }
  };

  const handleDownload = async () => {
    try {
      const response = await candidateApi.downloadResume(id);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `resume_${candidate.first_name}_${candidate.last_name}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError('Could not download resume. File may not exist.');
    }
  };

  if (loading) return <p>Loading candidate details...</p>;
  if (error && !candidate) return <p style={{ color: 'red' }}>{error}</p>;
  if (!candidate) return <p>Candidate not found.</p>;

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto' }}>
      <h2>Candidate Details</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {success && <p style={{ color: 'green' }}>{success}</p>}

       
      <div style={{ border: '1px solid #ddd', padding: '15px', borderRadius: '5px' }}>
        <p><strong>Name:</strong> {candidate.first_name} {candidate.last_name}</p>
        <p><strong>Email:</strong> {candidate.email}</p>
        <p><strong>Mobile:</strong> {candidate.mobile_number}</p>
        <p><strong>Current Company:</strong> {candidate.current_company || 'N/A'}</p>
        <p><strong>Total Experience:</strong> {candidate.total_experience} years</p>
        <p><strong>Applied Job ID:</strong> {candidate.applied_job_id}</p>
        <p><strong>Current Status:</strong> <span style={{ background: '#e0e0e0', padding: '3px 8px', borderRadius: '4px' }}>{candidate.status}</span></p>
      </div>

   
      <div style={{ marginTop: '25px', padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
        <h3>Resume</h3>
        {candidate.resume_file_id ? (
          <div>
            <p>Resume uploaded.</p>
            <button onClick={handleDownload} style={{ padding: '8px 16px' }}>
              Download Resume
            </button>
          </div>
        ) : (
          <p>No resume uploaded yet.</p>
        )}

        {canManage && (
          <div style={{ marginTop: '10px' }}>
            <input type="file" accept=".pdf" onChange={handleFileChange} />
            <button 
              onClick={handleUpload} 
              disabled={!selectedFile || uploading}
              style={{ marginLeft: '10px', padding: '6px 16px' }}
            >
              {uploading ? 'Uploading...' : 'Upload Resume'}
            </button>
            {selectedFile && <span style={{ marginLeft: '10px' }}>Selected: {selectedFile.name}</span>}
          </div>
        )}
      </div>

    
      {canManage && (
        <div style={{ marginTop: '25px', padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
          <h3>Update Status</h3>
          <form onSubmit={handleStatusUpdate}>
            <div>
              <label>New Status</label>
              <select
                value={newStatus}
                onChange={(e) => setNewStatus(e.target.value)}
                required
                style={{ width: '100%', padding: '8px', marginTop: '5px' }}
              >
                {CANDIDATE_STATUSES.map(opt => (
                  <option key={opt} value={opt}>{opt}</option>
                ))}
              </select>
            </div>
            <div style={{ marginTop: '10px' }}>
              <label>Notes (optional)</label>
              <textarea
                value={statusNotes}
                onChange={(e) => setStatusNotes(e.target.value)}
                rows="2"
                style={{ width: '100%', padding: '8px', marginTop: '5px' }}
                placeholder="Add any comments about this status change..."
              />
            </div>
            <button
              type="submit"
              disabled={updatingStatus}
              style={{ marginTop: '10px', padding: '8px 20px' }}
            >
              {updatingStatus ? 'Updating...' : 'Update Status'}
            </button>
          </form>
        </div>
      )}

   
      <div style={{ marginTop: '25px', padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
        <h3>Status History</h3>
        {history.length === 0 ? (
          <p>No status changes recorded yet.</p>
        ) : (
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {history.map((item, index) => (
              <li key={index} style={{ borderBottom: '1px solid #eee', padding: '8px 0' }}>
                <strong>{item.status}</strong> – {new Date(item.changed_at).toLocaleString()}
                <br />
                <span style={{ fontSize: '0.9em', color: '#555' }}>
                  by {item.changed_by}
                  {item.notes && ` – Note: ${item.notes}`}
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>

      <button onClick={() => navigate('/candidates')} style={{ marginTop: '20px' }}>
        Back to Candidates
      </button>
    </div>
  );
};

export default CandidateDetails;