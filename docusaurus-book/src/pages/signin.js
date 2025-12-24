import React, { useState } from 'react';
import Layout from '@theme/Layout';

function Signin() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('Signing in...');
    try {
      const response = await fetch('/api/better-auth/signin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        if (data.token) { // Assuming the token is returned as 'token' in the response body
          localStorage.setItem('authToken', data.token);
          setMessage('Signin successful! Redirecting...');
          window.location.href = '/'; // Redirect to home page or dashboard
        } else {
          setMessage('Signin successful, but no token received. Redirecting...');
          window.location.href = '/';
        }
      } else {
        setMessage(`Signin failed: ${data.detail || JSON.stringify(data)}`);
      }
    } catch (error) {
      setMessage(`An error occurred: ${error.message}`);
    }
  };

  return (
    <Layout title="Sign In" description="Sign in to your account">
      <main className="container margin-vert--lg">
        <h1>Sign In</h1>
        <form onSubmit={handleSubmit}>
          <div className="margin-bottom--md">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              className="input--text"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="margin-bottom--md">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              className="input--text"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="button button--primary">Sign In</button>
        </form>
        {message && <p className="margin-top--md">{message}</p>}
      </main>
    </Layout>
  );
}

export default Signin;
