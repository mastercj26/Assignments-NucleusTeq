import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import feedbackApi from '../api/feedbackapi'
import interviewApi from '../api/interviewapi'
import { getErrorMessage } from '../utils/errorHandler'
import { formatDate, isInterviewer, getUserId } from '../utils/helpers'
import { RECOMMENDATION_OPTIONS } from '../constants/candidateConstants'
import Alert from '../components/common/Alert'
import Select from '../components/common/Select'
import Textarea from '../components/common/Textarea'
import TagInput from '../components/common/TagInput'
import Button from '../components/common/Button'
import Loader from '../components/common/Loader'

const RATING_FIELDS = [
  { name: 'technical_rating', label: 'Technical Rating' },
  { name: 'communication_rating', label: 'Communication Rating' },
  { name: 'problem_solving_rating', label: 'Problem Solving Rating' },
]

const initialForm = {
  technical_rating: 0,
  communication_rating: 0,
  problem_solving_rating: 0,
  tech_areas_covered: [],
  comments: '',
  recommendation: '',
  interview_id: '',
}

function RatingField({ label, value, onChange, error }) {
  return (
    <div className="form-group">
      <label className="form-label">{label}<span className="required">*</span></label>
      <div className="rating-row">
        {[1, 2, 3, 4, 5].map((n) => (
          <button
            key={n}
            type="button"
            className={`rating-btn${value === n ? ' selected' : ''}`}
            onClick={() => onChange(n)}
          >
            {n}
          </button>
        ))}
      </div>
      {error && <p className="form-error">{error}</p>}
    </div>
  )
}

function SubmitFeedback() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [form, setForm] = useState({ ...initialForm, interview_id: id })
  const [errors, setErrors] = useState({})
  const [serverError, setServerError] = useState('')
  const [interview, setInterview] = useState(null)
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [accessDenied, setAccessDenied] = useState(false)

  useEffect(() => {
    interviewApi.get(id)
      .then((res) => {
        const iv = res.data
        if (isInterviewer() && iv.assigned_interviewer_id !== getUserId()) {
          setAccessDenied(true)
        }
        setInterview(iv)
      })
      .catch((err) => setServerError(getErrorMessage(err)))
      .finally(() => setLoading(false))
  }, [id])

  const validate = () => {
    const errs = {}
    if (!form.technical_rating) errs.technical_rating = 'Rating is required'
    if (!form.communication_rating) errs.communication_rating = 'Rating is required'
    if (!form.problem_solving_rating) errs.problem_solving_rating = 'Rating is required'
    if (form.tech_areas_covered.length === 0) errs.tech_areas_covered = 'At least one area is required'
    if (!form.recommendation) errs.recommendation = 'Recommendation is required'
    return errs
  }

  const handleRating = (field, value) => {
    setForm((prev) => ({ ...prev, [field]: value }))
    if (errors[field]) setErrors((prev) => ({ ...prev, [field]: '' }))
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setForm((prev) => ({ ...prev, [name]: value }))
    if (errors[name]) setErrors((prev) => ({ ...prev, [name]: '' }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const errs = validate()
    if (Object.keys(errs).length > 0) { setErrors(errs); return }

    setSubmitting(true)
    setServerError('')

    try {
      await feedbackApi.submit({
        interview_id: id,
        technical_rating: form.technical_rating,
        communication_rating: form.communication_rating,
        problem_solving_rating: form.problem_solving_rating,
        tech_areas_covered: form.tech_areas_covered,
        comments: form.comments || undefined,
        recommendation: form.recommendation,
      })
      navigate(`/interviews/${id}`)
    } catch (err) {
      setServerError(getErrorMessage(err))
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) return <Loader />
  if (accessDenied) return <Alert type="danger">You are not assigned to this interview and cannot submit feedback.</Alert>

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Submit Feedback</h1>
          {interview && (
            <p className="page-subtitle">
              Interview on {formatDate(interview.interview_date)} at {interview.interview_time}
            </p>
          )}
        </div>
      </div>

      <div className="card card-lg">
        <div className="card-body">
          {serverError && <Alert type="danger" onClose={() => setServerError('')}>{serverError}</Alert>}

          <form onSubmit={handleSubmit} noValidate>
            {RATING_FIELDS.map(({ name, label }) => (
              <RatingField
                key={name}
                label={label}
                value={form[name]}
                onChange={(val) => handleRating(name, val)}
                error={errors[name]}
              />
            ))}

            <TagInput
              label="Tech Areas Covered"
              value={form.tech_areas_covered}
              onChange={(areas) => { setForm((prev) => ({ ...prev, tech_areas_covered: areas })); setErrors((prev) => ({ ...prev, tech_areas_covered: '' })) }}
              error={errors.tech_areas_covered}
              required
              placeholder="e.g. React, Algorithms — press Enter to add"
            />

            <Select
              label="Recommendation"
              name="recommendation"
              value={form.recommendation}
              onChange={handleChange}
              error={errors.recommendation}
              required
            >
              <option value="">Select recommendation</option>
              {RECOMMENDATION_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </Select>

            <Textarea
              label="Comments"
              name="comments"
              value={form.comments}
              onChange={handleChange}
              rows={4}
              placeholder="Additional notes or observations (optional)"
            />

            <div className="form-actions">
              <Button type="submit" disabled={submitting}>
                {submitting ? 'Submitting…' : 'Submit Feedback'}
              </Button>
              <Button type="button" variant="secondary" onClick={() => navigate(`/interviews/${id}`)}>
                Cancel
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default SubmitFeedback
