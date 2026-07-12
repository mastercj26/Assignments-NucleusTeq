import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import userApi from '../api/userApi'
import { getErrorMessage } from '../utils/errorHandler'
import { validateNucleusEmail, validateName } from '../utils/validation'
import { ROLE_LABELS } from '../constants/roles'
import Alert from '../components/common/Alert'
import Input from '../components/common/Input'
import Select from '../components/common/Select'
import Button from '../components/common/Button'

const ROLES = ['admin', 'hr', 'interviewer']

function CreateUser() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    email: '',
    first_name: '',
    last_name: '',
    role: 'hr',
  })
  const [errors, setErrors] = useState({})
  const [serverError, setServerError] = useState('')
  const [loading, setLoading] = useState(false)

  const validate = () => {
    const errs = {}

    const emailErr = validateNucleusEmail(form.email)
    if (emailErr) errs.email = emailErr

    const fnErr = validateName(form.first_name, 'First name')
    if (fnErr) errs.first_name = fnErr

    const lnErr = validateName(form.last_name, 'Last name')
    if (lnErr) errs.last_name = lnErr

    if (!form.role) errs.role = 'Role is required'

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
      await userApi.create(form)
      navigate('/users')
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
          <h1 className="page-title">Create User</h1>
          <p className="page-subtitle">Add a new user to the system</p>
        </div>
      </div>

      <div className="card card-md">
        <div className="card-body">
          {serverError && <Alert type="danger" onClose={() => setServerError('')}>{serverError}</Alert>}

          <form onSubmit={handleSubmit} noValidate>
            <div className="form-row">
              <Input
                label="First Name"
                name="first_name"
                value={form.first_name}
                onChange={handleChange}
                error={errors.first_name}
                required
                placeholder="Min. 2 characters"
              />
              <Input
                label="Last Name"
                name="last_name"
                value={form.last_name}
                onChange={handleChange}
                error={errors.last_name}
                required
                placeholder="Min. 2 characters"
              />
            </div>

            <Input
              label="Email"
              name="email"
              type="email"
              value={form.email}
              onChange={handleChange}
              error={errors.email}
              required
              placeholder="user@nucleusteq.com"
              hint="Must end with @nucleusteq.com"
            />

            <Select label="Role" name="role" value={form.role} onChange={handleChange} error={errors.role} required>
              {ROLES.map((r) => (
                <option key={r} value={r}>{ROLE_LABELS[r]}</option>
              ))}
            </Select>

            <p className="form-note">
              The user will be created with the default password <strong>admin123</strong> and
              must set a new password on first sign-in.
            </p>

            <div className="form-actions">
              <Button type="submit" disabled={loading}>
                {loading ? 'Creating…' : 'Create User'}
              </Button>
              <Button type="button" variant="secondary" onClick={() => navigate('/users')}>
                Cancel
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default CreateUser
