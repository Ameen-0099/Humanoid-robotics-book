import React, { useState, useEffect } from 'react';
import Layout from '@theme/Layout';
import { useHistory } from '@docusaurus/router'; // Import main context hook
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

function Profile() {
  const [username, setUsername] = useState(null);
  const [email, setEmail] = useState(null);
  const history = useHistory();
  const { siteConfig } = useDocusaurusContext(); // Use Docusaurus context
  const { baseUrl } = siteConfig;

  useEffect(() => {
    const storedUsername = localStorage.getItem('username');
    const storedEmail = localStorage.getItem('email');

    if (storedUsername && storedEmail) {
      setUsername(storedUsername);
setEmail(storedEmail);
    } else {
      history.push(`${baseUrl}login`); // Use baseUrl from context
    }
  }, [history, baseUrl]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    localStorage.removeItem('email');
    history.push(`${baseUrl}login`); // Use baseUrl from context
  };

  if (!username || !email) {
    return (
      <Layout title="Profile">
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh', flexDirection: 'column' }}>
          <h1>Loading Profile...</h1>
        </div>
      </Layout>
    );
  }

  return (
    <Layout title="Profile">
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          height: '50vh',
          flexDirection: 'column',
        }}>
        <h1>Welcome, {username}!</h1>
        <p>Email: {email}</p>
        <button onClick={handleLogout}>Logout</button>
      </div>
    </Layout>
  );
}

export default Profile;