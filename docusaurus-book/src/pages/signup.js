import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { API_AUTH_SIGNUP } from '../utils/api';
import { useHistory } from '@docusaurus/router'; // Import main context hook
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

function SignUp() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState(null);
  const history = useHistory();
  const { siteConfig } = useDocusaurusContext(); // Use Docusaurus context
  const { baseUrl } = siteConfig;

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch(API_AUTH_SIGNUP, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, email, password }),
    });
    const data = await response.json();
    if (response.ok) {
      setMessage('Signup successful! Redirecting to login...');
      setTimeout(() => {
        history.push(`${baseUrl}login`); // Use baseUrl from context
      }, 2000);
    } else {
      let errorMessage = 'Signup failed.';
      if (data && data.detail) {
        errorMessage = `Signup failed: ${typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail)}`;
      } else if (data) {
        errorMessage = `Signup failed: ${JSON.stringify(data)}`;
      }
      setMessage(errorMessage);
    }
    console.log(data);
  };

  return (
    <Layout title="Sign Up">
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          height: '50vh',
          flexDirection: 'column',
        }}>
        <h1>Sign Up</h1>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button type="submit">Sign Up</button>
        </form>
        {message && <p>{message}</p>}
      </div>
    </Layout>
  );
}

export default SignUp;