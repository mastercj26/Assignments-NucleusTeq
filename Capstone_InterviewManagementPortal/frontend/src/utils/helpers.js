export const formatDate = (dateStr) => {
  if (!dateStr) return '—'
  try {
    return new Date(dateStr).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
  } catch {
    return dateStr
  }
}

export const formatDateTime = (dateStr) => {
  if (!dateStr) return '—'
  try {
    return new Date(dateStr).toLocaleString('en-US', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
  } catch {
    return dateStr
  }
}

export const getRole = () => localStorage.getItem('user_role') || ''
export const getUserId = () => localStorage.getItem('user_id') || ''
export const getUserEmail = () => localStorage.getItem('user_email') || ''

export const isAdmin = () => getRole() === 'admin'
export const isHR = () => getRole() === 'hr'
export const isInterviewer = () => getRole() === 'interviewer'
