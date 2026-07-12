import { useState, useEffect } from 'react'
import dashboardApi from '../api/dashboardapi'
import { getRole, getUserEmail } from '../utils/helpers'
import { ROLE_LABELS } from '../constants/roles'
import Loader from '../components/common/Loader'
import Alert from '../components/common/Alert'
import { getErrorMessage } from '../utils/errorHandler'

function StatCard({ label, value, colorClass }) {
  return (
    <div className={`stat-card ${colorClass || ''}`}>
      <div className="stat-label">{label}</div>
      <div className="stat-value">{value ?? '—'}</div>
    </div>
  )
}

function HRDashboard({ data }) {
  return (
    <div className="stats-grid">
      <StatCard label="Total Jobs" value={data.total_jobs} colorClass="c-primary" />
      <StatCard label="Total Candidates" value={data.total_candidates} />
      <StatCard label="Scheduled Interviews" value={data.scheduled_interviews} colorClass="c-warning" />
      <StatCard label="Selected" value={data.selected_candidates} colorClass="c-success" />
      <StatCard label="Rejected" value={data.rejected_candidates} colorClass="c-danger" />
    </div>
  )
}

function InterviewerDashboard({ data }) {
  return (
    <div className="stats-grid">
      <StatCard label="Assigned Interviews" value={data.assigned_interviews} colorClass="c-primary" />
      <StatCard label="Pending Feedback" value={data.pending_feedback} colorClass="c-warning" />
      <StatCard label="Completed" value={data.completed_feedback} colorClass="c-success" />
    </div>
  )
}

function Dashboard() {
  const role = getRole()
  const email = getUserEmail()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const load = async () => {
      try {
        let res
        if (role === 'interviewer') {
          res = await dashboardApi.getInterviewer()
        } else {
          res = await dashboardApi.getHR()
        }
        setData(res.data)
      } catch (err) {
        setError(getErrorMessage(err))
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [role])

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Dashboard</h1>
          <p className="page-subtitle">Welcome back, {email} · {ROLE_LABELS[role] || role}</p>
        </div>
      </div>

      {loading && <Loader />}
      {error && <Alert type="danger">{error}</Alert>}

      {data && role === 'interviewer' && <InterviewerDashboard data={data} />}
      {data && role !== 'interviewer' && <HRDashboard data={data} />}
    </div>
  )
}

export default Dashboard
