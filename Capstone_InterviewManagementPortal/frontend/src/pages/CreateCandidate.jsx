import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import candidateApi from '../api/candidateApi'
import jobApi from '../api/jobApi'
import { getErrorMessage } from '../utils/errorHandler'
import { validateNucleusEmail, validateMobile, validateName, validateExperience, validateRequired } from '../utils/validation'
import Alert from '../components/common/Alert'
import Input from '../components/common/Input'
import Select from '../components/common/Select'
import Button from '../components/common/Button'
import Loader from '../components/common/Loader'

const initialForm = {
  first_name: '',
  last_name: '',
  email: '',
  mobile_number: '',
  current_company: '',
  total_experience: '',
  applied_job_id: '',
}

function CreateCandidate() {
  const navigate = useNavigate()
  const [form, setForm] = useState(initialForm)
  const [errors, setErrors] = useState({})
  const [serverError, setServerError] = useState('')
  const [jobs, setJobs] = useState([])
  const [jobsLoading, setJobsLoading] = useState(true)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    jobApi.list(1, 100)
      .then((res) => {
        setJobs(res.data.jobs)
        if (res.data.jobs.length > 0) {
          setForm((prev) => ({ ...prev, applied_job_id: res.data.jobs[0].id }))
        }
      })
      .catch(() => setServerError('Could not load jobs. Please try again.'))
      .finally(() => setJobsLoading(false))
  }, [])

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

    setLoading(true)
    setServerError('')

    try {
      await candidateApi.create({ ...form, total_experience: Number(form.total_experience) })
      navigate('/candidates')
    } catch (err) {
      setServerError(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  if (jobsLoading) return <Loader />

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Add Candidate</h1>
          <p className="page-subtitle">Create a new candidate profile</p>
        </div>
      </div>

      <div className="card card-lg">
        <div className="card-body">
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
                placeholder="Min. 2 characters"
              />
              <Input
                label="Last Name"
                name="last_name"
                value={form.last_name}
                onChange={handleChange}
                error={errors.last_name}
                required
                placeholder="Min. 2 characters"
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
              placeholder="candidate@nucleusteq.com"
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
                placeholder="Exactly 10 digits"
                maxLength={10}
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
                placeholder="0 – 50"
              />
            </div>

            <Input
              label="Current Company"
              name="current_company"
              value={form.current_company}
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

            {jobs.length === 0 && (
              <Alert type="warning">No jobs available. Please create a job first.</Alert>
            )}

            <div className="form-actions">
              <Button type="submit" disabled={loading || jobs.length === 0}>
                {loading ? 'Creating…' : 'Create Candidate'}
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

export default CreateCandidate
