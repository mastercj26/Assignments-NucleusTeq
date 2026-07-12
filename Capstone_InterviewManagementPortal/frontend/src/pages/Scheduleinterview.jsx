import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import interviewApi from '../api/interviewapi'
import candidateApi from '../api/candidateApi'
import userApi from '../api/userApi'
import { getErrorMessage } from '../utils/errorHandler'
import { validateFutureDate } from '../utils/validation'
import Alert from '../components/common/Alert'
import Input from '../components/common/Input'
import Select from '../components/common/Select'
import TagInput from '../components/common/TagInput'
import Button from '../components/common/Button'
import Loader from '../components/common/Loader'

const initialForm = {
  candidate_id: '',
  job_id: '',
  interview_date: '',
  start_time: '',
  end_time: '',
  assigned_interviewer_id: '',
  focus_tech_areas: [],
}

function ScheduleInterview() {
  const navigate = useNavigate()
  const [form, setForm] = useState(initialForm)
  const [errors, setErrors] = useState({})
  const [serverError, setServerError] = useState('')
  const [loading, setLoading] = useState(false)

  const [candidates, setCandidates] = useState([])
  const [interviewers, setInterviewers] = useState([])
  const [dataLoading, setDataLoading] = useState(true)
  const [interviewerMode, setInterviewerMode] = useState('dropdown')

  useEffect(() => {
    const load = async () => {
      try {
        const candRes = await candidateApi.list(1, 100)
        setCandidates(candRes.data.candidates)
      } catch {
        setServerError('Could not load candidates.')
      }

      try {
        const res = await userApi.listInterviewers()
        setInterviewers(res.data)
      } catch {
        setInterviewerMode('text')
      }

      setDataLoading(false)
    }
    load()
  }, [])

  const validate = () => {
    const errs = {}
    if (!form.candidate_id) errs.candidate_id = 'Please select a candidate'
    if (!form.job_id.trim()) errs.job_id = 'Job ID is required'
    const dateErr = validateFutureDate(form.interview_date)
    if (dateErr) errs.interview_date = dateErr
    if (!form.start_time) errs.start_time = 'Start time is required'
    if (!form.end_time) errs.end_time = 'End time is required'
    else if (form.start_time && form.end_time <= form.start_time) errs.end_time = 'End time must be after start time'
    if (!form.assigned_interviewer_id.trim()) errs.assigned_interviewer_id = 'Interviewer is required'
    if (form.focus_tech_areas.length === 0) errs.focus_tech_areas = 'At least one focus area is required'
    return errs
  }

  useEffect(() => {
    if (!form.interview_date || !form.start_time || !form.end_time) return
    const params = {
      interview_date: new Date(form.interview_date).toISOString(),
      start_time: form.start_time,
      end_time: form.end_time,
    }
    userApi.listInterviewers(params)
      .then((res) => {
        setInterviewers(res.data)
        // clear the selection if that interviewer just became unavailable
        if (form.assigned_interviewer_id && !res.data.some((u) => u.id === form.assigned_interviewer_id)) {
          setForm((prev) => ({ ...prev, assigned_interviewer_id: '' }))
        }
      })
      .catch(() => {})
  }, [form.interview_date, form.start_time, form.end_time])

  const handleChange = (e) => {
    const { name, value } = e.target
    setForm((prev) => ({ ...prev, [name]: value }))
    if (errors[name]) setErrors((prev) => ({ ...prev, [name]: '' }))
  }

  const handleCandidateChange = (e) => {
    const candidateId = e.target.value
    const candidate = candidates.find((c) => c.id === candidateId)
    setForm((prev) => ({
      ...prev,
      candidate_id: candidateId,
      job_id: candidate?.applied_job_id || prev.job_id,
    }))
    if (errors.candidate_id) setErrors((prev) => ({ ...prev, candidate_id: '' }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const errs = validate()
    if (Object.keys(errs).length > 0) { setErrors(errs); return }

    setLoading(true)
    setServerError('')

    try {
      await interviewApi.schedule({
        candidate_id: form.candidate_id,
        job_id: form.job_id,
        interview_date: new Date(form.interview_date).toISOString(),
        start_time: form.start_time,
        end_time: form.end_time,
        assigned_interviewer_id: form.assigned_interviewer_id,
        focus_tech_areas: form.focus_tech_areas,
      })
      navigate('/interviews')
    } catch (err) {
      setServerError(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  if (dataLoading) return <Loader />

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Schedule Interview</h1>
          <p className="page-subtitle">Set up a new interview session</p>
        </div>
      </div>

      <div className="card card-xl">
        <div className="card-body">
          {serverError && <Alert type="danger" onClose={() => setServerError('')}>{serverError}</Alert>}

          <form onSubmit={handleSubmit} noValidate>
            <Select
              label="Candidate"
              name="candidate_id"
              value={form.candidate_id}
              onChange={handleCandidateChange}
              error={errors.candidate_id}
              required
            >
              <option value="">Select a candidate</option>
              {candidates.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.first_name} {c.last_name} — {c.email}
                </option>
              ))}
            </Select>

            <Input
              label="Job ID"
              name="job_id"
              value={form.job_id}
              onChange={handleChange}
              error={errors.job_id}
              required
              hint="Auto-filled from candidate's applied job. You can override it."
            />

            <div className="form-row">
              <Input
                label="Interview Date"
                name="interview_date"
                type="date"
                value={form.interview_date}
                onChange={handleChange}
                error={errors.interview_date}
                required
              />
              <Input
                label="Start Time"
                name="start_time"
                type="time"
                value={form.start_time}
                onChange={handleChange}
                error={errors.start_time}
                required
              />
              <Input
                label="End Time"
                name="end_time"
                type="time"
                value={form.end_time}
                onChange={handleChange}
                error={errors.end_time}
                required
              />
            </div>

            {interviewerMode === 'dropdown' && interviewers.length === 0 && form.interview_date && form.start_time && form.end_time && (
              <Alert type="warning">No interviewers are free at this time. Pick a different slot.</Alert>
            )}

            {interviewerMode === 'dropdown' && interviewers.length > 0 ? (
              <Select
                label="Interviewer"
                hint={form.interview_date && form.start_time && form.end_time
                  ? 'Showing interviewers free at the selected date and time'
                  : 'Pick a date and time to filter by availability'}
                name="assigned_interviewer_id"
                value={form.assigned_interviewer_id}
                onChange={handleChange}
                error={errors.assigned_interviewer_id}
                required
              >
                <option value="">Select an interviewer</option>
                {interviewers.map((iv) => (
                  <option key={iv.id} value={iv.id}>
                    {iv.first_name} {iv.last_name} — {iv.email}
                  </option>
                ))}
              </Select>
            ) : (
              <Input
                label="Interviewer ID"
                name="assigned_interviewer_id"
                value={form.assigned_interviewer_id}
                onChange={handleChange}
                error={errors.assigned_interviewer_id}
                required
                hint="Enter the interviewer's user ID"
              />
            )}

            <TagInput
              label="Focus Tech Areas"
              value={form.focus_tech_areas}
              onChange={(areas) => { setForm((prev) => ({ ...prev, focus_tech_areas: areas })); setErrors((prev) => ({ ...prev, focus_tech_areas: '' })) }}
              error={errors.focus_tech_areas}
              required
              placeholder="e.g. React, System Design — press Enter to add"
            />

            <div className="form-actions">
              <Button type="submit" disabled={loading}>
                {loading ? 'Scheduling…' : 'Schedule Interview'}
              </Button>
              <Button type="button" variant="secondary" onClick={() => navigate('/interviews')}>
                Cancel
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default ScheduleInterview
