import { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import candidateApi from '../api/candidateApi'
import { getErrorMessage } from '../utils/errorHandler'
import { isHR, formatDateTime } from '../utils/helpers'
import { validateFileSize } from '../utils/validation'
import { CANDIDATE_STATUSES, CANDIDATE_STATUS_LABELS, CANDIDATE_STATUS_BADGE } from '../constants/candidateConstants'
import Loader from '../components/common/Loader'
import Alert from '../components/common/Alert'
import Select from '../components/common/Select'
import Textarea from '../components/common/Textarea'
import Button from '../components/common/Button'

function CandidateDetails() {
  const { id } = useParams()
  const navigate = useNavigate()
  const fileRef = useRef(null)

  const [candidate, setCandidate] = useState(null)
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const [newStatus, setNewStatus] = useState('')
  const [statusNotes, setStatusNotes] = useState('')
  const [updatingStatus, setUpdatingStatus] = useState(false)

  const [selectedFile, setSelectedFile] = useState(null)
  const [fileError, setFileError] = useState('')
  const [uploading, setUploading] = useState(false)

  const canManage = isHR()

  const fetchData = async () => {
    setLoading(true)
    setError('')
    try {
      const [candRes, histRes] = await Promise.all([
        candidateApi.get(id),
        candidateApi.getStatusHistory(id),
      ])
      setCandidate(candRes.data)
      setNewStatus(candRes.data.status)
      setHistory(histRes.data.history || [])
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchData() }, [id]) // eslint-disable-line react-hooks/exhaustive-deps

  const handleStatusUpdate = async (e) => {
    e.preventDefault()
    setUpdatingStatus(true)
    setError('')
    setSuccess('')
    try {
      await candidateApi.updateStatus(id, newStatus, statusNotes)
      setSuccess('Status updated successfully.')
      setStatusNotes('')
      await fetchData()
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setUpdatingStatus(false)
    }
  }

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    setFileError('')
    if (!file) { setSelectedFile(null); return }
    if (file.type !== 'application/pdf') {
      setFileError('Only PDF files are allowed.')
      setSelectedFile(null)
      return
    }
    const sizeErr = validateFileSize(file, 5)
    if (sizeErr) {
      setFileError(sizeErr)
      setSelectedFile(null)
      return
    }
    setSelectedFile(file)
  }

  const handleUpload = async () => {
    if (!selectedFile) return
    setUploading(true)
    setError('')
    setSuccess('')
    try {
      await candidateApi.uploadResume(id, selectedFile)
      setSuccess('Resume uploaded successfully.')
      setSelectedFile(null)
      if (fileRef.current) fileRef.current.value = ''
      await fetchData()
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setUploading(false)
    }
  }

  const handleDownload = async () => {
    try {
      const res = await candidateApi.downloadResume(id)
      const url = window.URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }))
      const a = document.createElement('a')
      a.href = url
      a.download = `resume_${candidate.first_name}_${candidate.last_name}.pdf`
      document.body.appendChild(a)
      a.click()
      a.remove()
      window.URL.revokeObjectURL(url)
    } catch {
      setError('Could not download resume.')
    }
  }

  if (loading) return <Loader />
  if (error && !candidate) return <Alert type="danger">{error}</Alert>
  if (!candidate) return null

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">{candidate.first_name} {candidate.last_name}</h1>
          <p className="page-subtitle">{candidate.email}</p>
        </div>
        <div className="flex gap-2">
          {canManage && (
            <Link to={`/candidates/edit/${id}`}>
              <Button variant="secondary">Edit</Button>
            </Link>
          )}
          <Button variant="secondary" onClick={() => navigate('/candidates')}>Back</Button>
        </div>
      </div>

      {error && <Alert type="danger" onClose={() => setError('')}>{error}</Alert>}
      {success && <Alert type="success" onClose={() => setSuccess('')}>{success}</Alert>}

      <div className="grid-2col">
        <div className="card">
          <div className="card-header">
            <span className="card-title">Profile</span>
            <span className={`badge ${CANDIDATE_STATUS_BADGE[candidate.status] || 'badge-secondary'}`}>
              {CANDIDATE_STATUS_LABELS[candidate.status] || candidate.status}
            </span>
          </div>
          <div className="card-body">
            <div className="detail-grid">
              <div className="detail-item">
                <div className="detail-label">Mobile</div>
                <div className="detail-value">{candidate.mobile_number}</div>
              </div>
              <div className="detail-item">
                <div className="detail-label">Experience</div>
                <div className="detail-value">{candidate.total_experience} year(s)</div>
              </div>
              <div className="detail-item">
                <div className="detail-label">Current Company</div>
                <div className="detail-value">{candidate.current_company || '—'}</div>
              </div>
              <div className="detail-item">
                <div className="detail-label">Applied Job ID</div>
                <div className="detail-value text-sm text-muted">{candidate.applied_job_id}</div>
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <span className="card-title">Resume</span>
          </div>
          <div className="card-body">
            {candidate.resume_file_id ? (
              <div className="flex items-center gap-3 mb-4">
                <span className="text-sm text-muted">Resume uploaded</span>
                <Button variant="secondary" size="sm" onClick={handleDownload}>Download PDF</Button>
              </div>
            ) : (
              <p className="text-muted text-sm mb-4">No resume uploaded yet.</p>
            )}

            {canManage && (
              <div>
                <div className="form-group">
                  <label className="form-label">Upload Resume (PDF only)</label>
                  <input
                    ref={fileRef}
                    type="file"
                    accept=".pdf"
                    onChange={handleFileChange}
                    className="form-control"
                  />
                  {fileError && <p className="form-error">{fileError}</p>}
                </div>
                <Button
                  onClick={handleUpload}
                  disabled={!selectedFile || uploading}
                  size="sm"
                >
                  {uploading ? 'Uploading…' : 'Upload Resume'}
                </Button>
              </div>
            )}
          </div>
        </div>

        {canManage && (
          <div className="card">
            <div className="card-header">
              <span className="card-title">Update Status</span>
            </div>
            <div className="card-body">
              <form onSubmit={handleStatusUpdate} noValidate>
                <Select
                  label="New Status"
                  name="newStatus"
                  value={newStatus}
                  onChange={(e) => setNewStatus(e.target.value)}
                  required
                >
                  {CANDIDATE_STATUSES.map((s) => (
                    <option key={s} value={s}>{CANDIDATE_STATUS_LABELS[s]}</option>
                  ))}
                </Select>
                <Textarea
                  label="Notes"
                  name="statusNotes"
                  value={statusNotes}
                  onChange={(e) => setStatusNotes(e.target.value)}
                  rows={2}
                  placeholder="Optional notes about this status change"
                />
                <Button type="submit" disabled={updatingStatus} size="sm">
                  {updatingStatus ? 'Updating…' : 'Update Status'}
                </Button>
              </form>
            </div>
          </div>
        )}

        <div className={`card ${canManage ? '' : 'span-full'}`}>
          <div className="card-header">
            <span className="card-title">Status History</span>
          </div>
          <div className="card-body">
            {history.length === 0 ? (
              <p className="text-muted text-sm">No status changes recorded yet.</p>
            ) : (
              <div className="timeline">
                {history.map((item, i) => (
                  <div key={i} className="timeline-item">
                    <div className="timeline-dot" />
                    <div className="timeline-body">
                      <div className="timeline-status">{CANDIDATE_STATUS_LABELS[item.status] || item.status}</div>
                      <div className="timeline-meta">
                        {formatDateTime(item.changed_at)} &middot; by {item.changed_by}
                      </div>
                      {item.notes && <div className="timeline-notes">{item.notes}</div>}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default CandidateDetails
