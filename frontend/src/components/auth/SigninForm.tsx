// frontend/src/components/auth/SigninForm.tsx

import React, { useState } from 'react';
import { authAPI } from '../../services/api';
import { setAuth, isAuthenticated } from '../../services/auth';
import { useRouter } from 'next/router';

const SigninForm: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    // Validate inputs
    if (!email || !password) {
      setError('Please enter both email and password');
      setIsLoading(false);
      return;
    }

    // Validate password length (bcrypt has a 72-byte limit)
    if (password && password.length > 72) {
      setError('Password must not exceed 72 characters');
      setIsLoading(false);
      return;
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setError('Please enter a valid email address');
      setIsLoading(false);
      return;
    }

    try {
      const response = await authAPI.signin(email, password);

      // Store the auth token and user info
      setAuth(response.access_token, response.user);

      // Wait a brief moment to ensure token is stored
      await new Promise(resolve => setTimeout(resolve, 100));

      // Redirect to the todos page
      router.push('/todos');
    } catch (err: any) {
      console.error('Signin error:', err);
      if (err.message && err.message.includes('72 bytes')) {
        setError('Password must not exceed 72 characters');
      } else if (err.message && err.message.includes('Invalid credentials')) {
        setError('Invalid email or password. Please try again.');
      } else if (err.message && err.message.includes('connection')) {
        setError('Failed to connect to server. Please check your connection and try again.');
      } else {
        setError(err.message || 'An error occurred during signin. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6 text-center">Sign In</h2>

      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="email" className="block text-gray-700 text-sm font-bold mb-2">
            Email
          </label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="your@email.com"
            disabled={isLoading}
          />
        </div>

        <div className="mb-6">
          <div className="flex justify-between items-center mb-2">
            <label htmlFor="password" className="block text-gray-700 text-sm font-bold">
              Password
            </label>
            <span className={`text-xs ${password.length > 72 ? 'text-red-500' : 'text-gray-500'}`}>
              {password.length}/72
            </span>
          </div>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              password.length > 72 ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="Your password (max 72 characters)"
            disabled={isLoading}
          />
        </div>

        <button
          type="submit"
          className={`w-full bg-blue-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
            isLoading ? 'opacity-70 cursor-not-allowed' : 'hover:bg-blue-600'
          }`}
          disabled={isLoading}
        >
          {isLoading ? 'Signing in...' : 'Sign In'}
        </button>
      </form>

      <div className="mt-4 text-center">
        <p className="text-gray-600">
          Don't have an account?{' '}
          <a href="/signup" className="text-blue-500 hover:text-blue-700 font-medium">
            Sign up
          </a>
        </p>
      </div>
    </div>
  );
};

export default SigninForm;