import { useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { useDelayedNavigate } from '../hooks/useDelayedNavigate'
import api from '../api/axiosConfig'
import { getErrorMessage } from '../utils/errorHandler'
import { validatePassword } from '../utils/validation'
import Alert from '../components/common/Alert'
import Input from '../components/common/Input'
import Button from '../components/common/Button'

function ResetPassword() {
  const { state } = useLocation()
  const navigate = useNavigate()
  const delayedNavigate = useDelayedNavigate()
  const email = state?.email || localStorage.getItem('reset_email') || ''

  const [form, setForm] = useState({ oldPassword: '', newPassword: '', confirmPassword: '' })
  const [errors, setErrors] = useState({})
  const [serverError, setServerError] = useState('')
  const [success, setSuccess] = useState(false)
  const [loading, setLoading] = useState(false)

  const validate = () => {
    const errs = {}
    if (!form.oldPassword) errs.oldPassword = 'Current password is required'
    const pwErr = validatePassword(form.newPassword, form.confirmPassword)
    if (pwErr) errs.newPassword = pwErr
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
      await api.post('/auth/reset-password', {
        email,
        old_password: form.oldPassword,
        new_password: form.newPassword,
      })
      setSuccess(true)
      delayedNavigate('/login', 2500)
    } catch (err) {
      setServerError(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-logo">IMP</div>
        <h1 className="auth-title">Reset Password</h1>
        <p className="auth-subtitle">
          {email ? `Setting new password for ${email}` : 'Set a new password for your account'}
        </p>

        {success && <Alert type="success">Password reset successfully! Redirecting to login…</Alert>}
        {serverError && <Alert type="danger" onClose={() => setServerError('')}>{serverError}</Alert>}

        {!success && (
          <form onSubmit={handleSubmit} noValidate>
            <Input
              label="Current Password"
              name="oldPassword"
              type="password"
              value={form.oldPassword}
              onChange={handleChange}
              error={errors.oldPassword}
              required
              autoComplete="current-password"
            />
            <Input
              label="New Password"
              name="newPassword"
              type="password"
              value={form.newPassword}
              onChange={handleChange}
              error={errors.newPassword}
              required
              autoComplete="new-password"
              hint="6–12 characters. Letters, numbers, and @#$%^&+=! only."
            />
            <Input
              label="Confirm New Password"
              name="confirmPassword"
              type="password"
              value={form.confirmPassword}
              onChange={handleChange}
              required
              autoComplete="new-password"
            />
            <Button type="submit" disabled={loading} className="btn-block btn-lg">
              {loading ? 'Saving…' : 'Reset Password'}
            </Button>
          </form>
        )}
      </div>
    </div>
  )
}

export default ResetPassword
