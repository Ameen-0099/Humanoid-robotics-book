import React, { useState } from 'react';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

import { authClient } from '../utils/authClient';

function Signup() {
  const { siteConfig } = useDocusaurusContext();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [softwareBackground, setSoftwareBackground] = useState('');
  const [hardwareBackground, setHardwareBackground] = useState('');
  const [message, setMessage] = useState('');

  const handleSignup = async (event) => {
    event.preventDefault();
    setMessage('Signing up...');

    try {
      const { data, error } = await authClient.signUp.email({
        name,
        email,
        password,
        softwareBackground,
        hardwareBackground,
      });

      console.log('Signup Response Data:', data);

      if (error) {
        setMessage(`Signup failed: ${error.message}`);
      } else {
        setMessage('Signup successful! Please log in.');
        window.location.href = '/login';
      }
    } catch (error) {
      console.error('Signup error:', error);
      setMessage(`An error occurred during signup: ${error.message || 'Network error'}`);
    }
  };

  return (
    <Layout title="Sign Up" description="Sign up for an account">
      <main className="container margin-vert--lg">
        <div className="row">
          <div className="col col--6 col--offset-3">
            <h1>Sign Up</h1>
            <form onSubmit={handleSignup}>
              <div className="margin-bottom--md">
                <input
                  type="text"
                  className="form-control"
                  placeholder="Name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />
              </div>
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
              <div className="margin-bottom--md">
                <input
                  type="text"
                  className="form-control"
                  placeholder="Software Background (e.g., Python, C++)"
                  value={softwareBackground}
                  onChange={(e) => setSoftwareBackground(e.target.value)}
                />
              </div>
              <div className="margin-bottom--md">
                <input
                  type="text"
                  className="form-control"
                  placeholder="Hardware Background (e.g., Robotics, Embedded Systems)"
                  value={hardwareBackground}
                  onChange={(e) => setHardwareBackground(e.target.value)}
                />
              </div>
              <button type="submit" className="button button--primary button--block">
                Sign Up
              </button>
            </form>
            {message && <p className="margin-top--md">{message}</p>}
            <p className="margin-top--md">
              Already have an account? <a href="/login">Log In</a>
            </p>
          </div>
        </div>
      </main>
    </Layout>
  );
}

export default Signup;