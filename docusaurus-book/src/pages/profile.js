import React, { useState, useEffect } from 'react';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import useBaseUrl from '@docusaurus/useBaseUrl';
import Link from '@docusaurus/Link';

function Profile() {
  const { siteConfig } = useDocusaurusContext();
  const [user, setUser] = useState(null);
  const [message, setMessage] = useState('Loading profile...');
  const loginUrl = useBaseUrl('/login');

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
                  console.log('User data from API:', data);
                  setUser(data);
                  console.log('User object after setting state:', user);
                  setMessage('');
                } else {          setMessage(`Failed to load profile: ${response.statusText}`);
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
      <main className="profile-container">
        <div className="profile-card">
          {message && <p>{message}</p>}
          {user && (
            <div>
              <div className="profile-header">
                <h1 className="profile-title">{user.name || 'User Profile'}</h1>
                <p className="profile-email">{user.email}</p>
              </div>
              <div className="profile-details">
                {user.software_background && <p><strong>Software Background:</strong> {user.software_background}</p>}
                {user.hardware_background && <p><strong>Hardware Background:</strong> {user.hardware_background}</p>}
              </div>
              <button onClick={handleLogout} className="profile-logout-button">
                Log Out
              </button>
              <Link to="/update-profile" className="button button--secondary button--md">
                Update Profile
              </Link>
            </div>
          )}
          {!user && !message && (
            <div style={{ textAlign: 'center' }}>
              <p>Please <Link to="/login">log in</Link> to view your profile.</p>
            </div>
          )}
        </div>
      </main>
    </Layout>
  );
}

export default Profile;