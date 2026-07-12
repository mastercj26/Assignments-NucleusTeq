export const CANDIDATE_STATUSES = [
  'PROFILE_CREATED',
  'INTERVIEW_SCHEDULED',
  'INTERVIEW_COMPLETED',
  'SELECTED',
  'REJECTED',
]

export const CANDIDATE_STATUS_LABELS = {
  PROFILE_CREATED: 'Profile Created',
  INTERVIEW_SCHEDULED: 'Interview Scheduled',
  INTERVIEW_COMPLETED: 'Interview Completed',
  SELECTED: 'Selected',
  REJECTED: 'Rejected',
}

export const CANDIDATE_STATUS_BADGE = {
  PROFILE_CREATED: 'badge-info',
  INTERVIEW_SCHEDULED: 'badge-warning',
  INTERVIEW_COMPLETED: 'badge-secondary',
  SELECTED: 'badge-success',
  REJECTED: 'badge-danger',
}

export const INTERVIEW_STATUSES = {
  SCHEDULED: 'scheduled',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled',
}

export const INTERVIEW_STATUS_BADGE = {
  scheduled: 'badge-warning',
  completed: 'badge-success',
  cancelled: 'badge-danger',
}

export const RECOMMENDATION_OPTIONS = [
  { value: 'NEXT_ROUND', label: 'Next Round' },
  { value: 'SELECT', label: 'Select' },
  { value: 'REJECT', label: 'Reject' },
]
