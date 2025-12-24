import React, { useState } from 'react';
import Layout from '@theme/Layout';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

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
        window.location.href = '/profile'; // Redirect to profile page
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
      <main className="container margin-vert--lg">
        <div className="row">
          <div className="col col--6 col--offset-3">
            <h1>Log In</h1>
            <form onSubmit={handleLogin}>
              <div className="margin-bottom--md">
                <input
                  type="email"
                  className="form-control"
                  placeholder="Email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div className="margin-bottom--md">
                <input
                  type="password"
                  className="form-control"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
              <button type="submit" className="button button--primary button--block">
                Log In
              </button>
            </form>
            {message && <p className="margin-top--md">{message}</p>}
            <p className="margin-top--md">
              Don't have an account? <a href="/signup">Sign Up</a>
            </p>
          </div>
        </div>
      </main>
    </Layout>
  );
}

export default Login;