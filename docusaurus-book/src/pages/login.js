import React, { useState } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
import { useAuth } from '../contexts/AuthContext';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const profileUrl = useBaseUrl('/profile');
  const { login } = useAuth();

  const handleLogin = async (event) => {
    event.preventDefault();
    setMessage('Logging in...');

    try {
      const response = await fetch('http://127.0.0.1:8000/api/auth/sign-in/email-and-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      const data = await response.json();
      console.log('Login Response Data:', data);

      if (!response.ok) {
        // Handle HTTP errors
        throw new Error(data.detail || 'Login failed');
      }

      await login(data.access_token);
      setMessage('Login successful!');
      window.location.href = profileUrl; // Redirect to profile page
    } catch (error) {
      console.error('Login error:', error);
      setMessage(error.message || 'An error occurred during login.');
    }
  };

  return (
    <Layout title="Log In" description="Log in to your account">
      <div className="auth-container">
        <div className="auth-card">
          <h1 className="auth-title">Log In</h1>
          <form onSubmit={handleLogin}>
            <div className="auth-form-group">
              <label htmlFor="email">Email</label>
              <input
                id="email"
                type="email"
                className="auth-input"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="auth-form-group">
              <label htmlFor="password">Password</label>
              <input
                id="password"
                type="password"
                className="auth-input"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            {message && <p className="auth-message">{message}</p>}
            <button type="submit" className="auth-button">
              Log In
            </button>
          </form>
          <p className="auth-link">
            Don't have an account? <Link to="/signup">Sign Up</Link>
          </p>
        </div>
      </div>
    </Layout>
  );
}

export default Login;