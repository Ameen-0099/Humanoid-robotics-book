import React, { useState } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
// import { useAuth } from '../contexts/AuthContext'; // No longer needed for signup

function Signup() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [softwareBackground, setSoftwareBackground] = useState('');
  const [hardwareBackground, setHardwareBackground] = useState('');
  const [message, setMessage] = useState('');
  const loginUrl = useBaseUrl('/login');
  // const { authClient } = useAuth(); // No longer needed for signup

  const handleSignup = async (event) => {
    event.preventDefault();
    setMessage('Signing up...');

    try {
      const response = await fetch('http://127.0.0.1:8000/api/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name,
          email,
          password,
          software_background: softwareBackground,
          hardware_background: hardwareBackground,
        }),
      });

      const data = await response.json();
      console.log('Signup Response Data:', data);

      if (!response.ok) {
        // Handle HTTP errors
        throw new Error(data.detail || 'Signup failed');
      }

      setMessage('Signup successful! Please log in.');
      window.location.href = loginUrl;
    } catch (error) {
      console.error('Signup error:', error);
      setMessage(`An error occurred during signup: ${error.message || 'Network error'}`);
    }
  };

  return (
    <Layout title="Sign Up" description="Sign up for an account">
      <div className="auth-container">
        <div className="auth-card">
          <h1 className="auth-title">Create Account</h1>
          <form onSubmit={handleSignup}>
            <div className="auth-form-group">
              <label htmlFor="name">Full Name</label>
              <input
                id="name"
                type="text"
                className="auth-input"
                placeholder="John Doe"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
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
            <div className="auth-form-group">
              <label htmlFor="software">Software Background</label>
              <input
                id="software"
                type="text"
                className="auth-input"
                placeholder="e.g., Python, C++, ROS"
                value={softwareBackground}
                onChange={(e) => setSoftwareBackground(e.target.value)}
              />
            </div>
            <div className="auth-form-group">
              <label htmlFor="hardware">Hardware Background</label>
              <input
                id="hardware"
                type="text"
                className="auth-input"
                placeholder="e.g., Robotics, Arduino, Embedded Systems"
                value={hardwareBackground}
                onChange={(e) => setHardwareBackground(e.target.value)}
              />
            </div>
            {message && <p className="auth-message">{message}</p>}
            <button type="submit" className="auth-button">
              Sign Up
            </button>
          </form>
          <p className="auth-link">
            Already have an account? <Link to="/login">Log In</Link>
          </p>
        </div>
      </div>
    </Layout>
  );
}

export default Signup;
