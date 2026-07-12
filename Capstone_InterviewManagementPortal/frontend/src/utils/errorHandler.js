export const getErrorMessage = (error) => {
  if (!error.response) return 'Network error. Please check your connection.'

  const { data } = error.response

  if (data?.detail) {
    if (Array.isArray(data.detail)) {
      return data.detail.map((e) => e.msg || e.message || String(e)).join(', ')
    }
    return String(data.detail)
  }

  if (data?.message) return String(data.message)

  return 'Something went wrong. Please try again.'
}
