import React, { useState, useEffect } from 'react';
import Layout from '@theme/Layout';
import useBaseUrl from '@docusaurus/useBaseUrl';
import { useAuth } from '../contexts/AuthContext';

function UpdateProfile() {
  const { user, loading, fetchUser } = useAuth();
  const [name, setName] = useState('');
  const [softwareBackground, setSoftwareBackground] = useState('');
  const [hardwareBackground, setHardwareBackground] = useState('');
  const [message, setMessage] = useState('');
  const profileUrl = useBaseUrl('/profile');

  useEffect(() => {
    if (user) {
      setName(user.name || '');
      setSoftwareBackground(user.software_background || '');
      setHardwareBackground(user.hardware_background || '');
    }
  }, [user]);

  const handleUpdate = async (event) => {
    event.preventDefault();
    setMessage('Updating profile...');

    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('http://127.0.0.1:8000/api/auth/users/me/', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          name,
          software_background: softwareBackground,
          hardware_background: hardwareBackground,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to update profile');
      }

      await fetchUser(); // Refetch user data to update context
      setMessage('Profile updated successfully!');
      window.location.href = profileUrl;
    } catch (error) {
      console.error('Update profile error:', error);
      setMessage(error.message || 'An error occurred during update.');
    }
  };

  if (loading) {
    return <Layout title="Update Profile"><div className="auth-container"><p>Loading...</p></div></Layout>;
  }

  if (!user) {
    return <Layout title="Update Profile"><div className="auth-container"><p>You must be logged in to update your profile.</p></div></Layout>;
  }

  return (
    <Layout title="Update Profile" description="Update your user profile">
      <div className="auth-container">
        <div className="auth-card">
          <h1 className="auth-title">Update Profile</h1>
          <form onSubmit={handleUpdate}>
            <div className="auth-form-group">
              <label htmlFor="name">Full Name</label>
              <input
                id="name"
                type="text"
                className="auth-input"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
            <div className="auth-form-group">
              <label htmlFor="software">Software Background</label>
              <input
                id="software"
                type="text"
                className="auth-input"
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
                value={hardwareBackground}
                onChange={(e) => setHardwareBackground(e.target.value)}
              />
            </div>
            {message && <p className="auth-message">{message}</p>}
            <button type="submit" className="auth-button">
              Update Profile
            </button>
          </form>
        </div>
      </div>
    </Layout>
  );
}

export default UpdateProfile;
