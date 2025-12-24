import React, { useState, useEffect } from 'react';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import useBaseUrl from '@docusaurus/useBaseUrl';
import Link from '@docusaurus/Link';

function Profile() {
  const { siteConfig } = useDocusaurusContext();
  const [user, setUser] = useState(null);
  const [message, setMessage] = useState('Loading profile...');
  const loginUrl = useBaseUrl('/humanoid-robotics-book/login');

  useEffect(() => {
    const fetchProfile = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) {
        setMessage('You are not logged in.');
        return;
      }

      const API_BASE_URL = siteConfig.customFields.apiBaseUrl;
      const profileEndpoint = `${API_BASE_URL}/api/auth/users/me/`;

      try {
        const response = await fetch(profileEndpoint, {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          setUser(data);
          setMessage('');
        } else {
          setMessage(`Failed to load profile: ${response.statusText}`);
          localStorage.removeItem('access_token'); // Clear invalid token
        }
      } catch (error) {
        console.error('Profile fetch error:', error);
        setMessage('An error occurred while loading your profile.');
      }
    };

    fetchProfile();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    window.location.href = loginUrl;
  };

  return (
    <Layout title="Profile" description="User Profile">
      <main className="container margin-vert--lg">
        <div className="row">
          <div className="col col--6 col--offset-3">
            <h1>User Profile</h1>
            {message && <p>{message}</p>}
            {user && (
              <div>
                <p><strong>Email:</strong> {user.email}</p>
                <p><strong>Username:</strong> {user.username}</p>
                {user.software_background && <p><strong>Software Background:</strong> {user.software_background}</p>}
                {user.hardware_background && <p><strong>Hardware Background:</strong> {user.hardware_background}</p>}
                <button onClick={handleLogout} className="button button--danger">
                  Log Out
                </button>
              </div>
            )}
            {!user && !message && (
              <p>Please <Link to="/humanoid-robotics-book/login">log in</Link> to view your profile.</p>
            )}
          </div>
        </div>
      </main>
    </Layout>
  );
}

export default Profile;