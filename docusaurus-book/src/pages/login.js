import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { API_AUTH_LOGIN } from '../utils/api'; // Import the API endpoint

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch(API_AUTH_LOGIN, { // Use the imported constant
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });
    const data = await response.json();
    if (response.ok) {
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('username', data.username); // Store username
      localStorage.setItem('email', data.email);     // Store email
      setMessage('Login successful!');
    } else {
      let errorMessage = 'Login failed.';
      if (data && data.detail) {
        errorMessage = `Login failed: ${typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail)}`;
      } else if (data) {
        errorMessage = `Login failed: ${JSON.stringify(data)}`;
      }
      setMessage(errorMessage);
    }
    console.log(data);
  };

  return (
    <Layout title="Login">
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          height: '50vh',
          flexDirection: 'column',
        }}>
        <h1>Login</h1>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button type="submit">Login</button>
        </form>
        {message && <p>{message}</p>}
      </div>
    </Layout>
  );
}

export default Login;