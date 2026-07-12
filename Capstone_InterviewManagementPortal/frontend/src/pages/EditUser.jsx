import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useDelayedNavigate } from '../hooks/useDelayedNavigate'
import userApi from '../api/userApi'
import { getErrorMessage } from '../utils/errorHandler'
import { validateName } from '../utils/validation'
import { ROLE_LABELS } from '../constants/roles'
import Alert from '../components/common/Alert'
import Input from '../components/common/Input'
import Select from '../components/common/Select'
import Button from '../components/common/Button'
import Loader from '../components/common/Loader'

function EditUser() {
  const { id } = useParams()
  const navigate = useNavigate()
  const delayedNavigate = useDelayedNavigate()
  const [form, setForm] = useState({ first_name: '', last_name: '', role: '', status: '' })
  const [errors, setErrors] = useState({})
  const [serverError, setServerError] = useState('')
  const [success, setSuccess] = useState(false)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    userApi.get(id)
      .then((res) => {
        const { first_name, last_name, role, status } = res.data
        setForm({ first_name: first_name || '', last_name: last_name || '', role, status })
      })
      .catch((err) => setServerError(getErrorMessage(err)))
      .finally(() => setLoading(false))
  }, [id])

  const validate = () => {
    const errs = {}
    const fnErr = validateName(form.first_name, 'First name')
    if (fnErr) errs.first_name = fnErr
    const lnErr = validateName(form.last_name, 'Last name')
    if (lnErr) errs.last_name = lnErr
    if (!form.role) errs.role = 'Role is required'
    if (!form.status) errs.status = 'Status is required'
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

    setSaving(true)
    setServerError('')

    try {
      await userApi.update(id, form)
      setSuccess(true)
      delayedNavigate('/users', 1500)
    } catch (err) {
      setServerError(getErrorMessage(err))
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <Loader />

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Edit User</h1>
          <p className="page-subtitle">Update user details</p>
        </div>
      </div>

      <div className="card card-md">
        <div className="card-body">
          {success && <Alert type="success">User updated successfully! Redirecting…</Alert>}
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
              />
              <Input
                label="Last Name"
                name="last_name"
                value={form.last_name}
                onChange={handleChange}
                error={errors.last_name}
                required
              />
            </div>

            <Select label="Role" name="role" value={form.role} onChange={handleChange} error={errors.role} required>
              <option value="admin">{ROLE_LABELS.admin}</option>
              <option value="hr">{ROLE_LABELS.hr}</option>
              <option value="interviewer">{ROLE_LABELS.interviewer}</option>
            </Select>

            <Select label="Status" name="status" value={form.status} onChange={handleChange} error={errors.status} required>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
            </Select>

            <div className="form-actions">
              <Button type="submit" disabled={saving}>
                {saving ? 'Saving…' : 'Save Changes'}
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

export default EditUser
