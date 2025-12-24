import React, { useState } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const profileUrl = useBaseUrl('/humanoid-robotics-book/profile');

  const handleLogin = async (event) => {
    event.preventDefault();
    setMessage('Logging in...');

    try {
      const details = {
        'username': email,
        'password': password
      };
      const formBody = new URLSearchParams(details);

      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formBody,
      });

      let data;
      try {
        data = await response.json();
      } catch {
        throw new Error("Invalid JSON response from server");
      }

      if (response.ok) {
        localStorage.setItem('auth_session', JSON.stringify({ ...data, email }));
        localStorage.setItem('access_token', data.access_token);
        setMessage('Login successful!');
        window.location.href = profileUrl; // Redirect to profile page
      } else {
        setMessage(`Login failed: ${data.message || response.statusText}`);
      }
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
            Don't have an account? <Link to="/humanoid-robotics-book/signup">Sign Up</Link>
          </p>
        </div>
      </div>
    </Layout>
  );
}

export default Login;