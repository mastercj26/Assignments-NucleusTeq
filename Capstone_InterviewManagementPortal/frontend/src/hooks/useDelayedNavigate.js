import { useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'

// navigate after a small delay (used to show success message first).
// clears the timer on unmount so it doesn't redirect from some other page.
export const useDelayedNavigate = () => {
  const navigate = useNavigate()
  const timerRef = useRef(null)

  useEffect(() => () => clearTimeout(timerRef.current), [])

  return (path, delay = 1500) => {
    clearTimeout(timerRef.current)
    timerRef.current = setTimeout(() => navigate(path), delay)
  }
}
