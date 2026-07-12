import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import jobApi from '../api/jobApi'
import { getErrorMessage } from '../utils/errorHandler'
import { isHR } from '../utils/helpers'
import Loader from '../components/common/Loader'
import Alert from '../components/common/Alert'
import Button from '../components/common/Button'

function JobDetails() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [job, setJob] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    jobApi.get(id)
      .then((res) => setJob(res.data))
      .catch((err) => setError(getErrorMessage(err)))
      .finally(() => setLoading(false))
  }, [id])

  if (loading) return <Loader />
  if (error) return <Alert type="danger">{error}</Alert>
  if (!job) return null

  const statusBadge = (status) => {
    const map = { open: 'badge-success', closed: 'badge-danger', draft: 'badge-secondary' }
    return <span className={`badge ${map[status] || 'badge-secondary'}`}>{status}</span>
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">{job.job_title}</h1>
          <p className="page-subtitle">{job.job_role} &middot; {job.location}</p>
        </div>
        <div className="flex gap-2">
          {isHR() && (
            <Link to={`/jobs/edit/${id}`}>
              <Button variant="secondary">Edit Job</Button>
            </Link>
          )}
          <Button variant="secondary" onClick={() => navigate('/jobs')}>Back</Button>
        </div>
      </div>

      <div className="grid-2col">
        <div className="card">
          <div className="card-header">
            <span className="card-title">Job Details</span>
            {statusBadge(job.status)}
          </div>
          <div className="card-body">
            <div className="detail-grid">
              <div className="detail-item">
                <div className="detail-label">Employment Type</div>
                <div className="detail-value">{job.employment_type}</div>
              </div>
              <div className="detail-item">
                <div className="detail-label">Experience Required</div>
                <div className="detail-value">{job.experience_required} year(s)</div>
              </div>
              <div className="detail-item">
                <div className="detail-label">Location</div>
                <div className="detail-value">{job.location}</div>
              </div>
              <div className="detail-item">
                <div className="detail-label">Status</div>
                <div className="detail-value capitalize">{job.status}</div>
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <span className="card-title">Required Skills</span>
          </div>
          <div className="card-body">
            {job.required_skills.length === 0 ? (
              <p className="text-muted">No skills listed</p>
            ) : (
              <div className="tags mt-0">
                {job.required_skills.map((skill) => (
                  <span key={skill} className="tag">{skill}</span>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="card span-full">
          <div className="card-header">
            <span className="card-title">Description</span>
          </div>
          <div className="card-body">
            <p className="job-details-text">{job.job_details}</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default JobDetails
