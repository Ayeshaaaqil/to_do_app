// frontend/src/services/auth.ts

// Store the authentication token
let authToken: string | null = null;

// Store user info
let userInfo: { id: string; email: string; name: string } | null = null;

// Check if we're in a browser environment
const isBrowser = typeof window !== 'undefined';

// Check if user is authenticated
export const isAuthenticated = (): boolean => {
  if (isBrowser) {
    // Always check localStorage first to ensure we have the latest value
    const storedToken = localStorage.getItem('authToken');
    if (storedToken) {
      // Update module-level token if needed
      if (storedToken !== authToken) {
        authToken = storedToken;
      }
      return true;
    }
  }
  return authToken !== null;
};

// Get the current auth token
export const getAuthToken = (): string | null => {
  if (isBrowser) {
    // Always check localStorage first to ensure we have the latest value
    const storedToken = localStorage.getItem('authToken');
    if (storedToken) {
      // Update module-level token if needed
      if (storedToken !== authToken) {
        authToken = storedToken;
      }
      return storedToken;
    }
  }
  return authToken;
};

// Helper function to validate JWT token format
function isValidToken(token: string): boolean {
  try {
    // Basic JWT format validation: 3 parts separated by dots
    const parts = token.split('.');
    if (parts.length !== 3) {
      return false;
    }

    // Try to decode the payload part
    const payload = parts[1];
    const decodedPayload = atob(payload.replace(/-/g, '+').replace(/_/g, '/'));
    const parsedPayload = JSON.parse(decodedPayload);

    // Check if token has expiration
    if (parsedPayload.exp) {
      const currentTime = Math.floor(Date.now() / 1000);
      // Check if token is expired
      if (parsedPayload.exp < currentTime) {
        return false;
      }
    }

    return true;
  } catch (e) {
    // If decoding fails, the token might still be valid but not in standard JWT format
    // For now, we'll consider it valid if it's a non-empty string
    return token && token.length > 0;
  }
}

// Get user info
export const getUserInfo = () => {
  if (isBrowser) {
    // Always check localStorage first to ensure we have the latest value
    const storedUser = localStorage.getItem('userInfo');
    if (storedUser) {
      try {
        // Update module-level userInfo if needed
        if (storedUser !== JSON.stringify(userInfo)) {
          userInfo = JSON.parse(storedUser);
        }
        return JSON.parse(storedUser);
      } catch (e) {
        console.error('Error parsing user info from localStorage:', e);
        // Clear the corrupted data
        localStorage.removeItem('userInfo');
        return null;
      }
    }
  }
  return userInfo;
};

// Set authentication token and user info
export const setAuth = (token: string, user: { id: string; email: string; name: string }) => {
  // Store in localStorage for persistence (only in browser)
  if (isBrowser) {
    localStorage.setItem('authToken', token);
    localStorage.setItem('userInfo', JSON.stringify(user));
  }

  // Update module-level variables
  authToken = token;
  userInfo = user;
};

// Clear authentication
export const clearAuth = () => {
  // Remove from localStorage (only in browser)
  if (isBrowser) {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userInfo');
  }

  // Clear module-level variables
  authToken = null;
  userInfo = null;
};

// Initialize auth from localStorage
export const initAuth = () => {
  if (!isBrowser) return; // Skip initialization if not in browser

  const storedToken = localStorage.getItem('authToken');
  const storedUser = localStorage.getItem('userInfo');

  if (storedToken) {
    authToken = storedToken;
  }

  if (storedUser) {
    try {
      userInfo = JSON.parse(storedUser);
    } catch (e) {
      console.error('Error parsing user info from localStorage:', e);
      // Clear the corrupted data
      localStorage.removeItem('userInfo');
      userInfo = null;
    }
  }
};

// Initialize on module load (only in browser)
if (isBrowser) {
  initAuth();
} else {
  // For server-side rendering, ensure variables are initialized
  authToken = null;
  userInfo = null;
}