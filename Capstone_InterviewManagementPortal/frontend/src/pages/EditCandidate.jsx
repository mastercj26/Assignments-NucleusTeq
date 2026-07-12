import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useDelayedNavigate } from '../hooks/useDelayedNavigate'
import candidateApi from '../api/candidateApi'
import jobApi from '../api/jobApi'
import { getErrorMessage } from '../utils/errorHandler'
import { validateNucleusEmail, validateMobile, validateName, validateExperience, validateRequired } from '../utils/validation'
import { CANDIDATE_STATUSES, CANDIDATE_STATUS_LABELS } from '../constants/candidateConstants'
import Alert from '../components/common/Alert'
import Input from '../components/common/Input'
import Select from '../components/common/Select'
import Button from '../components/common/Button'
import Loader from '../components/common/Loader'

function EditCandidate() {
  const { id } = useParams()
  const navigate = useNavigate()
  const delayedNavigate = useDelayedNavigate()
  const [form, setForm] = useState(null)
  const [jobs, setJobs] = useState([])
  const [errors, setErrors] = useState({})
  const [serverError, setServerError] = useState('')
  const [success, setSuccess] = useState(false)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    Promise.all([candidateApi.get(id), jobApi.list(1, 100)])
      .then(([candRes, jobsRes]) => {
        setForm(candRes.data)
        setJobs(jobsRes.data.jobs)
      })
      .catch((err) => setServerError(getErrorMessage(err)))
      .finally(() => setLoading(false))
  }, [id])

  const validate = () => {
    const errs = {}

    const fnErr = validateName(form.first_name, 'First name')
    if (fnErr) errs.first_name = fnErr

    const lnErr = validateName(form.last_name, 'Last name')
    if (lnErr) errs.last_name = lnErr

    const emailErr = validateNucleusEmail(form.email)
    if (emailErr) errs.email = emailErr

    const mobileErr = validateMobile(form.mobile_number)
    if (mobileErr) errs.mobile_number = mobileErr

    const expErr = validateExperience(form.total_experience)
    if (expErr) errs.total_experience = expErr

    const jobErr = validateRequired(form.applied_job_id, 'Applied job')
    if (jobErr) errs.applied_job_id = jobErr

    return errs
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

    setSaving(true)
    setServerError('')

    try {
      await candidateApi.update(id, { ...form, total_experience: Number(form.total_experience) })
      setSuccess(true)
      delayedNavigate('/candidates', 1500)
    } catch (err) {
      setServerError(getErrorMessage(err))
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <Loader />
  if (!form && serverError) return <Alert type="danger">{serverError}</Alert>

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Edit Candidate</h1>
          <p className="page-subtitle">Update candidate profile</p>
        </div>
      </div>

      <div className="card card-lg">
        <div className="card-body">
          {success && <Alert type="success">Candidate updated! Redirecting…</Alert>}
          {serverError && <Alert type="danger" onClose={() => setServerError('')}>{serverError}</Alert>}

          <form onSubmit={handleSubmit} noValidate>
            <div className="form-row">
              <Input
                label="First Name"
                name="first_name"
                value={form.first_name}
                onChange={handleChange}
                error={errors.first_name}
                required
              />
              <Input
                label="Last Name"
                name="last_name"
                value={form.last_name}
                onChange={handleChange}
                error={errors.last_name}
                required
              />
            </div>

            <Input
              label="Email"
              name="email"
              type="email"
              value={form.email}
              onChange={handleChange}
              error={errors.email}
              required
              hint="Must end with @nucleusteq.com"
            />

            <div className="form-row">
              <Input
                label="Mobile Number"
                name="mobile_number"
                type="tel"
                value={form.mobile_number}
                onChange={handleChange}
                error={errors.mobile_number}
                required
                maxLength={10}
                placeholder="Exactly 10 digits"
              />
              <Input
                label="Total Experience (years)"
                name="total_experience"
                type="number"
                value={form.total_experience}
                onChange={handleChange}
                error={errors.total_experience}
                required
                min="0"
                max="50"
                step="0.5"
              />
            </div>

            <Input
              label="Current Company"
              name="current_company"
              value={form.current_company || ''}
              onChange={handleChange}
              placeholder="Optional"
            />

            <Select
              label="Applied Job"
              name="applied_job_id"
              value={form.applied_job_id}
              onChange={handleChange}
              error={errors.applied_job_id}
              required
            >
              <option value="">Select a job</option>
              {jobs.map((job) => (
                <option key={job.id} value={job.id}>{job.job_title}</option>
              ))}
            </Select>

            <Select label="Status" name="status" value={form.status} onChange={handleChange}>
              {CANDIDATE_STATUSES.map((s) => (
                <option key={s} value={s}>{CANDIDATE_STATUS_LABELS[s]}</option>
              ))}
            </Select>

            <div className="form-actions">
              <Button type="submit" disabled={saving}>
                {saving ? 'Saving…' : 'Save Changes'}
              </Button>
              <Button type="button" variant="secondary" onClick={() => navigate('/candidates')}>
                Cancel
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default EditCandidate
