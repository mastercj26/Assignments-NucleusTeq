import { useNavigate } from 'react-router-dom'
import { getUserEmail, getRole } from '../../utils/helpers'
import { ROLE_LABELS } from '../../constants/roles'

function Header() {
  const navigate = useNavigate()
  const email = getUserEmail()
  const role = getRole()

  const handleLogout = () => {
    localStorage.clear()
    navigate('/login')
  }

  return (
    <header className="app-header">
      <span className="header-title">Interview Management Portal</span>
      <div className="header-right">
        <span className="header-user">{email}</span>
        <span className="header-role">{ROLE_LABELS[role] || role}</span>
        <button type="button" className="btn btn-secondary btn-sm" onClick={handleLogout}>
          Logout
        </button>
      </div>
    </header>
  )
}

export default Header
