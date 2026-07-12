import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useDelayedNavigate } from '../hooks/useDelayedNavigate'
import jobApi from '../api/jobApi'
import { getErrorMessage } from '../utils/errorHandler'
import { validateExperience } from '../utils/validation'
import Alert from '../components/common/Alert'
import Input from '../components/common/Input'
import Select from '../components/common/Select'
import Textarea from '../components/common/Textarea'
import TagInput from '../components/common/TagInput'
import Button from '../components/common/Button'
import Loader from '../components/common/Loader'

const EMPLOYMENT_TYPES = ['Full Time', 'Internship']
const STATUSES = ['open', 'closed', 'draft']

function EditJob() {
  const { id } = useParams()
  const navigate = useNavigate()
  const delayedNavigate = useDelayedNavigate()
  const [form, setForm] = useState(null)
  const [errors, setErrors] = useState({})
  const [serverError, setServerError] = useState('')
  const [success, setSuccess] = useState(false)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    jobApi.get(id)
      .then((res) => setForm(res.data))
      .catch((err) => setServerError(getErrorMessage(err)))
      .finally(() => setLoading(false))
  }, [id])

  const validate = () => {
    const errs = {}
    if (!form.job_title.trim()) errs.job_title = 'Job title is required'
    if (!form.job_details.trim()) errs.job_details = 'Job details are required'
    if (!form.job_role.trim()) errs.job_role = 'Job role is required'
    if (!form.location.trim()) errs.location = 'Location is required'
    if (form.required_skills.length === 0) errs.required_skills = 'At least one skill is required'
    const expErr = validateExperience(form.experience_required)
    if (expErr) errs.experience_required = expErr
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
      await jobApi.update(id, { ...form, experience_required: Number(form.experience_required) })
      setSuccess(true)
      delayedNavigate('/jobs', 1500)
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
          <h1 className="page-title">Edit Job</h1>
          <p className="page-subtitle">Update job description</p>
        </div>
      </div>

      <div className="card card-xl">
        <div className="card-body">
          {success && <Alert type="success">Job updated successfully! Redirecting…</Alert>}
          {serverError && <Alert type="danger" onClose={() => setServerError('')}>{serverError}</Alert>}

          <form onSubmit={handleSubmit} noValidate>
            <div className="form-row">
              <Input
                label="Job Title"
                name="job_title"
                value={form.job_title}
                onChange={handleChange}
                error={errors.job_title}
                required
              />
              <Input
                label="Job Role"
                name="job_role"
                value={form.job_role}
                onChange={handleChange}
                error={errors.job_role}
                required
              />
            </div>

            <Textarea
              label="Job Details"
              name="job_details"
              value={form.job_details}
              onChange={handleChange}
              error={errors.job_details}
              required
              rows={4}
            />

            <div className="form-row-3">
              <Input
                label="Experience (years)"
                name="experience_required"
                type="number"
                value={form.experience_required}
                onChange={handleChange}
                error={errors.experience_required}
                min="0"
                max="50"
                step="0.5"
              />
              <Select
                label="Employment Type"
                name="employment_type"
                value={form.employment_type}
                onChange={handleChange}
              >
                {EMPLOYMENT_TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
              </Select>
              <Select
                label="Status"
                name="status"
                value={form.status}
                onChange={handleChange}
              >
                {STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
              </Select>
            </div>

            <Input
              label="Location"
              name="location"
              value={form.location}
              onChange={handleChange}
              error={errors.location}
              required
            />

            <TagInput
              label="Required Skills"
              value={form.required_skills}
              onChange={(skills) => { setForm((prev) => ({ ...prev, required_skills: skills })); setErrors((prev) => ({ ...prev, required_skills: '' })) }}
              error={errors.required_skills}
              required
            />

            <div className="form-actions">
              <Button type="submit" disabled={saving}>
                {saving ? 'Saving…' : 'Save Changes'}
              </Button>
              <Button type="button" variant="secondary" onClick={() => navigate('/jobs')}>
                Cancel
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default EditJob
