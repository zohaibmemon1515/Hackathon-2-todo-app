// Authentication state management utilities

// Get the current authentication token
export const getAuthToken = (): string | null => {
  return typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
};

// Set the authentication token
export const setAuthToken = (token: string): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('access_token', token);
  }
};

// Remove the authentication token
export const removeAuthToken = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('access_token');
  }
};

// Check if the user is authenticated
export const isAuthenticated = (): boolean => {
  const token = getAuthToken();
  return token !== null && token.length > 0;
};

// Get user profile from token (this would require decoding the JWT)
// For now, we'll just return a simple check
export const getCurrentUser = () => {
  if (!isAuthenticated()) {
    return null;
  }

  // In a real implementation, you might decode the JWT to get user info
  // or make an API call to get user profile
  return {
    token: getAuthToken(),
    // This would be decoded from the JWT in a real implementation
    // For now, we'll just return basic structure
  };
};