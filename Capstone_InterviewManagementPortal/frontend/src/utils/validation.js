
export const validatePassword = (password, confirmPassword = '') => {
  if (password.length < 6 || password.length > 12) {
    return 'Password must be 6–12 characters long.';
  }
  if (!/^[A-Za-z0-9@#$%^&+=!]{6,12}$/.test(password)) {
    return 'Password must contain only letters, numbers, or special characters (@#$%^&+=!).';
  }
  if (confirmPassword && password !== confirmPassword) {
    return 'Passwords do not match.';
  }
  return null;
};