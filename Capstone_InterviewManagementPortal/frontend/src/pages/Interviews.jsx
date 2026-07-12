import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import interviewApi from '../api/interviewapi'
import { getErrorMessage } from '../utils/errorHandler'
import { isHR, formatDate } from '../utils/helpers'
import { INTERVIEW_STATUS_BADGE } from '../constants/candidateConstants'
import Loader from '../components/common/Loader'
import Alert from '../components/common/Alert'
import Pagination from '../components/common/Pagination'
import Button from '../components/common/Button'

function Interviews() {
  const [interviews, setInterviews] = useState([])
  const [page, setPage] = useState(1)
  const [meta, setMeta] = useState({ total: 0, pages: 1, per_page: 10 })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const canSchedule = isHR()

  useEffect(() => {
    setLoading(true)
    setError('')
    interviewApi.list(page)
      .then((res) => {
        setInterviews(res.data.interviews)
        setMeta({ total: res.data.total, pages: res.data.pages, per_page: res.data.per_page })
      })
      .catch((err) => setError(getErrorMessage(err)))
      .finally(() => setLoading(false))
  }, [page])

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Interviews</h1>
          <p className="page-subtitle">
            {canSchedule ? 'Manage all interview schedules' : 'Your assigned interviews'}
          </p>
        </div>
        {canSchedule && (
          <Link to="/interviews/schedule">
            <Button>Schedule Interview</Button>
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
                    <th>Candidate ID</th>
                    <th>Date</th>
                    <th>Time</th>
                    <th>Interviewer ID</th>
                    <th>Focus Areas</th>
                    <th>Status</th>
                    <th className="text-right">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {interviews.length === 0 ? (
                    <tr>
                      <td colSpan={7}>
                        <div className="empty-state">
                          <div className="empty-state-title">No interviews found</div>
                          {canSchedule && <p className="empty-state-sub">Schedule the first interview.</p>}
                        </div>
                      </td>
                    </tr>
                  ) : (
                    interviews.map((iv) => (
                      <tr key={iv.id}>
                        <td className="text-sm text-muted">{iv.candidate_id}</td>
                        <td>{formatDate(iv.interview_date)}</td>
                        <td>{iv.interview_time}</td>
                        <td className="text-sm text-muted">{iv.assigned_interviewer_id}</td>
                        <td>
                          <div className="tags mt-0">
                            {iv.focus_tech_areas.slice(0, 2).map((a) => (
                              <span key={a} className="tag">{a}</span>
                            ))}
                            {iv.focus_tech_areas.length > 2 && (
                              <span className="tag">+{iv.focus_tech_areas.length - 2}</span>
                            )}
                          </div>
                        </td>
                        <td>
                          <span className={`badge ${INTERVIEW_STATUS_BADGE[iv.status] || 'badge-secondary'}`}>
                            {iv.status}
                          </span>
                        </td>
                        <td>
                          <div className="table-actions justify-end">
                            <Link to={`/interviews/${iv.id}`}>
                              <Button variant="secondary" size="sm">View</Button>
                            </Link>
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

export default Interviews
