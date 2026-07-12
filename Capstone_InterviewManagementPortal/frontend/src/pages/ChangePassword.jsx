import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useDelayedNavigate } from '../hooks/useDelayedNavigate'
import api from '../api/axiosConfig'
import { getErrorMessage } from '../utils/errorHandler'
import { validatePassword } from '../utils/validation'
import { getUserEmail } from '../utils/helpers'
import Alert from '../components/common/Alert'
import Input from '../components/common/Input'
import Button from '../components/common/Button'

function ChangePassword() {
  const navigate = useNavigate()
  const delayedNavigate = useDelayedNavigate()
  const email = getUserEmail()

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
      delayedNavigate('/dashboard', 2000)
    } catch (err) {
      setServerError(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Change Password</h1>
          <p className="page-subtitle">Update your account password</p>
        </div>
      </div>

      <div className="card card-sm">
        <div className="card-body">
          {success && <Alert type="success">Password changed! Redirecting to dashboard…</Alert>}
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
              <div className="form-actions">
                <Button type="submit" disabled={loading}>
                  {loading ? 'Saving…' : 'Change Password'}
                </Button>
                <Button type="button" variant="secondary" onClick={() => navigate('/dashboard')}>
                  Cancel
                </Button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  )
}

export default ChangePassword
