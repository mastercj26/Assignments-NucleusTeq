import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import jobApi from '../api/jobApi'
import { getErrorMessage } from '../utils/errorHandler'
import { isHR } from '../utils/helpers'
import Loader from '../components/common/Loader'
import Alert from '../components/common/Alert'
import Pagination from '../components/common/Pagination'
import Button from '../components/common/Button'

function Jobs() {
  const [jobs, setJobs] = useState([])
  const [page, setPage] = useState(1)
  const [meta, setMeta] = useState({ total: 0, pages: 1, per_page: 10 })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const canManage = isHR()

  useEffect(() => {
    setLoading(true)
    setError('')
    jobApi.list(page)
      .then((res) => {
        setJobs(res.data.jobs)
        setMeta({ total: res.data.total, pages: res.data.pages, per_page: res.data.per_page })
      })
      .catch((err) => setError(getErrorMessage(err)))
      .finally(() => setLoading(false))
  }, [page])

  const statusBadge = (status) => {
    const map = { open: 'badge-success', closed: 'badge-danger', draft: 'badge-secondary' }
    return <span className={`badge ${map[status] || 'badge-secondary'}`}>{status}</span>
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Jobs</h1>
          <p className="page-subtitle">Manage job descriptions and openings</p>
        </div>
        {canManage && (
          <Link to="/jobs/create">
            <Button>Create Job</Button>
          </Link>
        )}
      </div>

      {error && <Alert type="danger">{error}</Alert>}

      <div className="card">
        {loading ? (
          <Loader />
        ) : (
          <>
            <div className="table-wrap">
              <table className="table">
                <thead>
                  <tr>
                    <th>Title</th>
                    <th>Role</th>
                    <th>Employment</th>
                    <th>Location</th>
                    <th>Experience</th>
                    <th>Status</th>
                    <th className="text-right">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {jobs.length === 0 ? (
                    <tr>
                      <td colSpan={7}>
                        <div className="empty-state">
                          <div className="empty-state-title">No jobs found</div>
                          {canManage && <p className="empty-state-sub">Create your first job posting.</p>}
                        </div>
                      </td>
                    </tr>
                  ) : (
                    jobs.map((job) => (
                      <tr key={job.id}>
                        <td className="font-medium">{job.job_title}</td>
                        <td>{job.job_role}</td>
                        <td>{job.employment_type}</td>
                        <td>{job.location}</td>
                        <td>{job.experience_required}y</td>
                        <td>{statusBadge(job.status)}</td>
                        <td>
                          <div className="table-actions justify-end">
                            <Link to={`/jobs/${job.id}`}>
                              <Button variant="secondary" size="sm">View</Button>
                            </Link>
                            {canManage && (
                              <Link to={`/jobs/edit/${job.id}`}>
                                <Button variant="secondary" size="sm">Edit</Button>
                              </Link>
                            )}
                          </div>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
            <Pagination
              page={page}
              pages={meta.pages}
              total={meta.total}
              perPage={meta.per_page}
              onPageChange={setPage}
            />
          </>
        )}
      </div>
    </div>
  )
}

export default Jobs
