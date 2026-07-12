import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import userApi from '../api/userApi'
import { getErrorMessage } from '../utils/errorHandler'
import { ROLE_LABELS } from '../constants/roles'
import Loader from '../components/common/Loader'
import Alert from '../components/common/Alert'
import Pagination from '../components/common/Pagination'
import Button from '../components/common/Button'

function Users() {
  const [users, setUsers] = useState([])
  const [page, setPage] = useState(1)
  const [meta, setMeta] = useState({ total: 0, pages: 1, per_page: 10 })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [toggleError, setToggleError] = useState('')

  const fetchUsers = async (p) => {
    setLoading(true)
    setError('')
    try {
      const res = await userApi.list(p)
      setUsers(res.data.users)
      setMeta({ total: res.data.total, pages: res.data.pages, per_page: res.data.per_page })
      setPage(res.data.page)
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchUsers(page) }, [page])

  const handleToggle = async (id, isActive) => {
    setToggleError('')
    try {
      await userApi.toggleStatus(id, !isActive)
      fetchUsers(page)
    } catch (err) {
      setToggleError(getErrorMessage(err))
    }
  }

  const statusBadge = (status) => {
    const map = { active: 'badge-success', inactive: 'badge-danger', first_login: 'badge-warning' }
    return <span className={`badge ${map[status] || 'badge-secondary'}`}>{status}</span>
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Users</h1>
          <p className="page-subtitle">Manage system users and roles</p>
        </div>
        <Link to="/users/create">
          <Button>Create User</Button>
        </Link>
      </div>

      {error && <Alert type="danger">{error}</Alert>}
      {toggleError && <Alert type="danger" onClose={() => setToggleError('')}>{toggleError}</Alert>}

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
                    <th>Role</th>
                    <th>Status</th>
                    <th>First Login</th>
                    <th className="text-right">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {users.length === 0 ? (
                    <tr>
                      <td colSpan={6}>
                        <div className="empty-state">
                          <div className="empty-state-title">No users found</div>
                        </div>
                      </td>
                    </tr>
                  ) : (
                    users.map((user) => (
                      <tr key={user.id}>
                        <td className="font-medium">{user.first_name} {user.last_name}</td>
                        <td className="text-muted">{user.email}</td>
                        <td>{ROLE_LABELS[user.role] || user.role}</td>
                        <td>{statusBadge(user.status)}</td>
                        <td>
                          {user.is_first_login
                            ? <span className="badge badge-warning">Pending</span>
                            : <span className="badge badge-success">Done</span>}
                        </td>
                        <td>
                          <div className="table-actions justify-end">
                            <Link to={`/users/edit/${user.id}`}>
                              <Button variant="secondary" size="sm">Edit</Button>
                            </Link>
                            <Button
                              variant={user.status === 'active' ? 'danger' : 'success'}
                              size="sm"
                              onClick={() => handleToggle(user.id, user.status === 'active')}
                            >
                              {user.status === 'active' ? 'Disable' : 'Enable'}
                            </Button>
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

export default Users
