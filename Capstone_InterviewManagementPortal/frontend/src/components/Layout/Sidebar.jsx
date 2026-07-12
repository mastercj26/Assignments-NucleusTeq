import { NavLink } from 'react-router-dom'
import { getRole } from '../../utils/helpers'

const ALL_NAV = [
  { to: '/dashboard', label: 'Dashboard', roles: ['admin', 'hr', 'interviewer'] },
  { to: '/users', label: 'Users', roles: ['admin'] },
  { to: '/jobs', label: 'Jobs', roles: ['admin', 'hr', 'interviewer'] },
  { to: '/candidates', label: 'Candidates', roles: ['admin', 'hr', 'interviewer'] },
  { to: '/interviews', label: 'Interviews', roles: ['admin', 'hr', 'interviewer'] },
]

function Sidebar() {
  const role = getRole()
  const navItems = ALL_NAV.filter((item) => item.roles.includes(role))

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="sidebar-brand-name">IMP</div>
        <div className="sidebar-brand-sub">Interview Management Portal</div>
      </div>

      <nav className="sidebar-nav">
        <div className="nav-section-label">Menu</div>
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}
          >
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <NavLink
          to="/change-password"
          className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}
        >
          Change Password
        </NavLink>
      </div>
    </aside>
  )
}

export default Sidebar
