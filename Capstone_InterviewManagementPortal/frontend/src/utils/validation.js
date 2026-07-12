// trim + lowercase emails in one place
export const normalizeEmail = (email) => (email || '').trim().toLowerCase()

export const validatePassword = (password, confirmPassword = '') => {
  if (!password) return 'Password is required'
  if (password.length < 6 || password.length > 12) return 'Password must be 6–12 characters'
  if (!/^[A-Za-z0-9@#$%^&+=!]{6,12}$/.test(password)) return 'Only letters, numbers, and @#$%^&+=! allowed'
  if (confirmPassword && password !== confirmPassword) return 'Passwords do not match'
  return null
}

export const validateEmail = (email) => {
  const value = normalizeEmail(email)
  if (!value) return 'Email is required'
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return 'Enter a valid email address'
  return null
}

export const validateNucleusEmail = (email) => {
  const base = validateEmail(email)
  if (base) return base
  const value = normalizeEmail(email)
  if (!value.endsWith('@nucleusteq.com')) return 'Email must be from nucleusteq.com domain'
  if (!/^[a-z0-9._]+@/.test(value)) return 'Email can only contain letters, numbers, dot or underscore'
  return null
}

export const validateMobile = (mobile) => {
  if (!mobile || !mobile.trim()) return 'Mobile number is required'
  if (!/^\d{10}$/.test(mobile.trim())) return 'Mobile number must be exactly 10 digits'
  return null
}

export const validateName = (value, label = 'This field') => {
  if (!value || !value.trim()) return `${label} is required`
  if (value.trim().length < 2) return `${label} must be at least 2 characters`
  if (!/^[A-Za-z ]+$/.test(value.trim())) return `${label} can only contain letters`
  if (!/^[A-Za-z\s'-]+$/.test(value.trim())) return `${label} can only contain letters, spaces, hyphens, and apostrophes`
  return null
}

export const validateExperience = (value) => {
  const n = Number(value)
  if (value === '' || value === null || value === undefined) return 'Experience is required'
  if (isNaN(n)) return 'Experience must be a number'
  if (n < 0) return 'Experience cannot be negative'
  if (n > 50) return 'Experience cannot exceed 50 years'
  return null
}

export const validateFutureDate = (dateStr) => {
  if (!dateStr) return 'Date is required'
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const selected = new Date(dateStr)
  if (isNaN(selected.getTime())) return 'Enter a valid date'
  if (selected < today) return 'Date must be today or in the future'
  return null
}

export const validateFileSize = (file, maxMB = 5) => {
  if (!file) return null
  if (file.size > maxMB * 1024 * 1024) return `File size must not exceed ${maxMB}MB`
  return null
}

export const validateRequired = (value, label = 'This field') => {
  if (value === null || value === undefined || String(value).trim() === '') return `${label} is required`
  return null
}
