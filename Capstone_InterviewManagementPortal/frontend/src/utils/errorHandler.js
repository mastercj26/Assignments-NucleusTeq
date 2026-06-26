export const getErrorMessage = (error) => {
  if (!error.response) {
    return 'Cannot connect to server. Please check your network.';
  }

  const { status, data } = error.response;

  // FastAPI validation error (422)
  if (status === 422 && data.detail && Array.isArray(data.detail)) {
    const firstError = data.detail[0];
    const field = firstError.loc[firstError.loc.length - 1];
    return `${field}: ${firstError.msg}`;
  }

  // Our global handler format
  if (data?.message) {
    return data.message;
  }

  // FastAPI simple error format
  if (data?.detail && typeof data.detail === 'string') {
    return data.detail;
  }

  return 'An unexpected error occurred';
};