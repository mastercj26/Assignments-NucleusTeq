import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import './styles/global.css'

import MainLayout from './components/Layout/MainLayout'
import Login from './pages/Login'
import ResetPassword from './pages/ResetPassword'
import Dashboard from './pages/Dashboard'
import Users from './pages/Users'
import CreateUser from './pages/CreateUser'
import EditUser from './pages/EditUser'
import Jobs from './pages/Jobs'
import CreateJob from './pages/CreateJob'
import EditJob from './pages/EditJob'
import JobDetails from './pages/JobDetails'
import Candidates from './pages/Candidates'
import CreateCandidate from './pages/CreateCandidate'
import EditCandidate from './pages/EditCandidate'
import CandidateDetails from './pages/CandidateDetails'
import Interviews from './pages/Interviews'
import ScheduleInterview from './pages/Scheduleinterview'
import InterviewDetails from './pages/InterviewDetails'
import SubmitFeedback from './pages/SubmitFeedback'
import ChangePassword from './pages/ChangePassword'

function ProtectedRoute({ children }) {
  const token = localStorage.getItem('access_token')
  if (!token) return <Navigate to="/login" replace />
  return children
}

function Protected({ children }) {
  return (
    <ProtectedRoute>
      <MainLayout>{children}</MainLayout>
    </ProtectedRoute>
  )
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/reset-password" element={<ResetPassword />} />

        <Route path="/" element={<Protected><Dashboard /></Protected>} />
        <Route path="/dashboard" element={<Protected><Dashboard /></Protected>} />

        <Route path="/users" element={<Protected><Users /></Protected>} />
        <Route path="/users/create" element={<Protected><CreateUser /></Protected>} />
        <Route path="/users/edit/:id" element={<Protected><EditUser /></Protected>} />

        <Route path="/jobs" element={<Protected><Jobs /></Protected>} />
        <Route path="/jobs/create" element={<Protected><CreateJob /></Protected>} />
        <Route path="/jobs/edit/:id" element={<Protected><EditJob /></Protected>} />
        <Route path="/jobs/:id" element={<Protected><JobDetails /></Protected>} />

        <Route path="/candidates" element={<Protected><Candidates /></Protected>} />
        <Route path="/candidates/create" element={<Protected><CreateCandidate /></Protected>} />
        <Route path="/candidates/edit/:id" element={<Protected><EditCandidate /></Protected>} />
        <Route path="/candidates/:id" element={<Protected><CandidateDetails /></Protected>} />

        <Route path="/interviews" element={<Protected><Interviews /></Protected>} />
        <Route path="/interviews/schedule" element={<Protected><ScheduleInterview /></Protected>} />
        <Route path="/interviews/:id" element={<Protected><InterviewDetails /></Protected>} />
        <Route path="/interviews/:id/feedback" element={<Protected><SubmitFeedback /></Protected>} />

        <Route path="/change-password" element={<Protected><ChangePassword /></Protected>} />

        <Route path="*" element={<Protected><div style={{ padding: 40 }}><h2>404 — Page Not Found</h2></div></Protected>} />
      </Routes>
    </Router>
  )
}

export default App
