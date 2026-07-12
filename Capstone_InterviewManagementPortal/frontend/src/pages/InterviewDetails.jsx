import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import interviewApi from '../api/interviewapi'
import feedbackApi from '../api/feedbackapi'
import { getErrorMessage } from '../utils/errorHandler'
import { isHR, isInterviewer, getUserId, formatDate, formatDateTime } from '../utils/helpers'
import { validateFutureDate } from '../utils/validation'
import { INTERVIEW_STATUS_BADGE } from '../constants/candidateConstants'
import Loader from '../components/common/Loader'
import Alert from '../components/common/Alert'
import Button from '../components/common/Button'
import Select from '../components/common/Select'
import TagInput from '../components/common/TagInput'

const INTERVIEW_STATUSES = ['scheduled', 'completed', 'cancelled']

function InterviewDetails() {
  const { id } = useParams()
  const navigate = useNavigate()

  const [interview, setInterview] = useState(null)
  const [feedback, setFeedback] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const [editing, setEditing] = useState(false)
  const [editForm, setEditForm] = useState({})
  const [saving, setSaving] = useState(false)

  const canManage = isHR()
  const isIv = isInterviewer()
  const [editErrors, setEditErrors] = useState({})

  const fetchData = async () => {
    setLoading(true)
    try {
      const ivRes = await interviewApi.get(id)
      setInterview(ivRes.data)
      setEditForm({
        interview_date: ivRes.data.interview_date?.split('T')[0] || '',
        interview_time: ivRes.data.interview_time || '',
        assigned_interviewer_id: ivRes.data.assigned_interviewer_id || '',
        focus_tech_areas: ivRes.data.focus_tech_areas || [],
        status: ivRes.data.status || 'scheduled',
      })

      try {
        const fbRes = await feedbackApi.getByInterview(id)
        setFeedback(fbRes.data)
      } catch {
        setFeedback(null)
      }
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchData() }, [id]) // eslint-disable-line react-hooks/exhaustive-deps

  const handleEditChange = (e) => {
    const { name, value } = e.target
    setEditForm((prev) => ({ ...prev, [name]: value }))
  }

  const handleSave = async (e) => {
    e.preventDefault()
    const errs = {}
    const dateErr = validateFutureDate(editForm.interview_date)
    if (dateErr) errs.interview_date = dateErr
    if (!editForm.interview_time) errs.interview_time = 'Time is required'
    if (!editForm.assigned_interviewer_id.trim()) errs.assigned_interviewer_id = 'Interviewer ID is required'
    if (Object.keys(errs).length > 0) { setEditErrors(errs); return }
    setEditErrors({})
    setSaving(true)
    setError('')
    try {
      await interviewApi.update(id, {
        interview_date: new Date(editForm.interview_date).toISOString(),
        interview_time: editForm.interview_time,
        assigned_interviewer_id: editForm.assigned_interviewer_id,
        focus_tech_areas: editForm.focus_tech_areas,
        status: editForm.status,
      })
      setSuccess('Interview updated.')
      setEditing(false)
      await fetchData()
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <Loader />
  if (error && !interview) return <Alert type="danger">{error}</Alert>
  if (!interview) return null

  const RECOMMENDATION_LABELS = { NEXT_ROUND: 'Next Round', SELECT: 'Select', REJECT: 'Reject' }

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Interview Details</h1>
          <p className="page-subtitle">Candidate ID: {interview.candidate_id}</p>
        </div>
        <div className="flex gap-2">
          {canManage && !editing && (
            <Button onClick={() => setEditing(true)}>Edit</Button>
          )}
          {isIv && interview.status === 'scheduled' && !feedback && getUserId() === interview.assigned_interviewer_id && (
            <Link to={`/interviews/${id}/feedback`}>
              <Button>Submit Feedback</Button>
            </Link>
          )}
          <Button variant="secondary" onClick={() => navigate('/interviews')}>Back</Button>
        </div>
      </div>

      {error && <Alert type="danger" onClose={() => setError('')}>{error}</Alert>}
      {success && <Alert type="success" onClose={() => setSuccess('')}>{success}</Alert>}

      {editing ? (
        <div className="card card-580 mb-16">
          <div className="card-header">
            <span className="card-title">Edit Interview</span>
          </div>
          <div className="card-body">
            <form onSubmit={handleSave} noValidate>
              <div className="form-row">
                <div className="form-group">
                  <label className="form-label">Date <span className="required">*</span></label>
                  <input
                    type="date"
                    name="interview_date"
                    value={editForm.interview_date}
                    onChange={handleEditChange}
                    className="form-control"
                  />
                  {editErrors.interview_date && <p className="form-error">{editErrors.interview_date}</p>}
                </div>
                <div className="form-group">
                  <label className="form-label">Time <span className="required">*</span></label>
                  <input
                    type="time"
                    name="interview_time"
                    value={editForm.interview_time}
                    onChange={handleEditChange}
                    className="form-control"
                  />
                  {editErrors.interview_time && <p className="form-error">{editErrors.interview_time}</p>}
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">Interviewer ID <span className="required">*</span></label>
                <input
                  type="text"
                  name="assigned_interviewer_id"
                  value={editForm.assigned_interviewer_id}
                  onChange={handleEditChange}
                  className="form-control"
                />
                {editErrors.assigned_interviewer_id && <p className="form-error">{editErrors.assigned_interviewer_id}</p>}
              </div>

              <Select label="Status" name="status" value={editForm.status} onChange={handleEditChange}>
                {INTERVIEW_STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
              </Select>

              <TagInput
                label="Focus Tech Areas"
                value={editForm.focus_tech_areas}
                onChange={(areas) => setEditForm((prev) => ({ ...prev, focus_tech_areas: areas }))}
              />

              <div className="form-actions">
                <Button type="submit" disabled={saving}>
                  {saving ? 'Saving…' : 'Save Changes'}
                </Button>
                <Button type="button" variant="secondary" onClick={() => setEditing(false)}>
                  Cancel
                </Button>
              </div>
            </form>
          </div>
        </div>
      ) : (
        <div className="grid-2col">
          <div className="card">
            <div className="card-header">
              <span className="card-title">Schedule</span>
              <span className={`badge ${INTERVIEW_STATUS_BADGE[interview.status] || 'badge-secondary'}`}>
                {interview.status}
              </span>
            </div>
            <div className="card-body">
              <div className="detail-grid">
                <div className="detail-item">
                  <div className="detail-label">Date</div>
                  <div className="detail-value">{formatDate(interview.interview_date)}</div>
                </div>
                <div className="detail-item">
                  <div className="detail-label">Time</div>
                  <div className="detail-value">{interview.interview_time}</div>
                </div>
                <div className="detail-item">
                  <div className="detail-label">Candidate ID</div>
                  <div className="detail-value text-sm text-muted">{interview.candidate_id}</div>
                </div>
                <div className="detail-item">
                  <div className="detail-label">Interviewer ID</div>
                  <div className="detail-value text-sm text-muted">{interview.assigned_interviewer_id}</div>
                </div>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="card-header">
              <span className="card-title">Focus Tech Areas</span>
            </div>
            <div className="card-body">
              <div className="tags mt-0">
                {interview.focus_tech_areas.map((a) => (
                  <span key={a} className="tag">{a}</span>
                ))}
              </div>
            </div>
          </div>

          <div className="card span-full">
            <div className="card-header">
              <span className="card-title">Feedback</span>
            </div>
            <div className="card-body">
              {!feedback ? (
                <div className="empty-state p-24">
                  <div className="empty-state-title">No feedback submitted yet</div>
                  {isIv && interview.status === 'scheduled' && getUserId() === interview.assigned_interviewer_id && (
                    <Link to={`/interviews/${id}/feedback`}>
                      <Button size="sm" className="mt-3">Submit Feedback</Button>
                    </Link>
                  )}
                </div>
              ) : (
                <div>
                  <div className="detail-grid mb-16">
                    <div className="detail-item">
                      <div className="detail-label">Technical Rating</div>
                      <div className="detail-value">{feedback.technical_rating} / 5</div>
                    </div>
                    <div className="detail-item">
                      <div className="detail-label">Communication Rating</div>
                      <div className="detail-value">{feedback.communication_rating} / 5</div>
                    </div>
                    <div className="detail-item">
                      <div className="detail-label">Problem Solving</div>
                      <div className="detail-value">{feedback.problem_solving_rating} / 5</div>
                    </div>
                    <div className="detail-item">
                      <div className="detail-label">Recommendation</div>
                      <div className="detail-value">
                        <span className={`badge ${feedback.recommendation === 'SELECT' ? 'badge-success' : feedback.recommendation === 'REJECT' ? 'badge-danger' : 'badge-warning'}`}>
                          {RECOMMENDATION_LABELS[feedback.recommendation] || feedback.recommendation}
                        </span>
                      </div>
                    </div>
                  </div>
                  {feedback.tech_areas_covered?.length > 0 && (
                    <div className="detail-item mb-12">
                      <div className="detail-label">Areas Covered</div>
                      <div className="tags mt-4">
                        {feedback.tech_areas_covered.map((a) => <span key={a} className="tag">{a}</span>)}
                      </div>
                    </div>
                  )}
                  {feedback.comments && (
                    <div className="detail-item">
                      <div className="detail-label">Comments</div>
                      <div className="detail-value pre-wrap">{feedback.comments}</div>
                    </div>
                  )}
                  <p className="text-muted text-sm mt-3">Submitted: {formatDateTime(feedback.submitted_at)}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default InterviewDetails
