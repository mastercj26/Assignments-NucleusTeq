import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import candidateApi from '../api/candidateApi'
import { getErrorMessage } from '../utils/errorHandler'
import { isHR } from '../utils/helpers'
import { CANDIDATE_STATUS_LABELS, CANDIDATE_STATUS_BADGE } from '../constants/candidateConstants'
import Loader from '../components/common/Loader'
import Alert from '../components/common/Alert'
import Pagination from '../components/common/Pagination'
import Button from '../components/common/Button'

function Candidates() {
  const [candidates, setCandidates] = useState([])
  const [page, setPage] = useState(1)
  const [meta, setMeta] = useState({ total: 0, pages: 1, per_page: 10 })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const canManage = isHR()

  useEffect(() => {
    setLoading(true)
    setError('')
    candidateApi.list(page)
      .then((res) => {
        setCandidates(res.data.candidates)
        setMeta({ total: res.data.total, pages: res.data.pages, per_page: res.data.per_page })
      })
      .catch((err) => setError(getErrorMessage(err)))
      .finally(() => setLoading(false))
  }, [page])

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Candidates</h1>
          <p className="page-subtitle">Manage candidate profiles and track progress</p>
        </div>
        {canManage && (
          <Link to="/candidates/create">
            <Button>Add Candidate</Button>
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
                    <th>Name</th>
                    <th>Email</th>
                    <th>Mobile</th>
                    <th>Experience</th>
                    <th>Status</th>
                    <th className="text-right">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {candidates.length === 0 ? (
                    <tr>
                      <td colSpan={6}>
                        <div className="empty-state">
                          <div className="empty-state-title">No candidates found</div>
                          {canManage && <p className="empty-state-sub">Add your first candidate profile.</p>}
                        </div>
                      </td>
                    </tr>
                  ) : (
                    candidates.map((c) => (
                      <tr key={c.id}>
                        <td className="font-medium">{c.first_name} {c.last_name}</td>
                        <td className="text-muted">{c.email}</td>
                        <td>{c.mobile_number}</td>
                        <td>{c.total_experience}y</td>
                        <td>
                          <span className={`badge ${CANDIDATE_STATUS_BADGE[c.status] || 'badge-secondary'}`}>
                            {CANDIDATE_STATUS_LABELS[c.status] || c.status}
                          </span>
                        </td>
                        <td>
                          <div className="table-actions justify-end">
                            <Link to={`/candidates/${c.id}`}>
                              <Button variant="secondary" size="sm">View</Button>
                            </Link>
                            {canManage && (
                              <Link to={`/candidates/edit/${c.id}`}>
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

export default Candidates
