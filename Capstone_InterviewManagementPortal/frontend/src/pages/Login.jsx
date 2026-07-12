import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/axiosConfig'
import { getErrorMessage } from '../utils/errorHandler'
import { normalizeEmail } from '../utils/validation'
import Alert from '../components/common/Alert'
import Input from '../components/common/Input'
import Button from '../components/common/Button'

function Login() {
  const navigate = useNavigate()
  const [form, setForm] = useState({ email: '', password: '' })
  const [errors, setErrors] = useState({})
  const [serverError, setServerError] = useState('')
  const [loading, setLoading] = useState(false)

  const validate = () => {
    const errs = {}
    if (!form.email.trim()) errs.email = 'Email is required'
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) errs.email = 'Invalid email address'
    if (!form.password) errs.password = 'Password is required'
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
      const res = await api.post('/auth/login', { email: normalizeEmail(form.email), password: form.password })
      const { access_token, user_id, email, role } = res.data
      localStorage.setItem('access_token', access_token)
      localStorage.setItem('user_id', user_id)
      localStorage.setItem('user_email', email)
      localStorage.setItem('user_role', role)
      navigate('/dashboard')
    } catch (err) {
      const msg = getErrorMessage(err)
      if (msg.toLowerCase().includes('reset your password')) {
        navigate('/reset-password', { state: { email: normalizeEmail(form.email) } })
      } else {
        setServerError(msg)
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-logo">IMP</div>
        <h1 className="auth-title">Sign in</h1>
        <p className="auth-subtitle">Interview Management Portal</p>

        {serverError && <Alert type="danger" onClose={() => setServerError('')}>{serverError}</Alert>}

        <form onSubmit={handleSubmit} noValidate autoComplete="off">
          <Input
            label="Email"
            name="email"
            type="email"
            value={form.email}
            onChange={handleChange}
            error={errors.email}
            required
            autoComplete="off"
            placeholder="you@nucleusteq.com"
          />
          <Input
            label="Password"
            name="password"
            type="password"
            value={form.password}
            onChange={handleChange}
            error={errors.password}
            required
            autoComplete="new-password"
            placeholder="Enter your password"
          />
          <Button type="submit" disabled={loading} className="btn-block btn-lg">
            {loading ? 'Signing in…' : 'Sign in'}
          </Button>
        </form>
      </div>
    </div>
  )
}

export default Login
