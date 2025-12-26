import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const { siteConfig } = useDocusaurusContext();

  const fetchUser = useCallback(async () => {
    const token = localStorage.getItem('access_token');
    if (token) {
      try {
        const API_BASE_URL = siteConfig.customFields.apiBaseUrl;
        const profileEndpoint = `${API_BASE_URL}/api/auth/users/me/`;
        const response = await fetch(profileEndpoint, {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const userData = await response.json();
          setUser(userData);
        } else {
          setUser(null);
          localStorage.removeItem('access_token');
        }
      } catch (error) {
        console.error("Failed to fetch user", error);
        setUser(null);
      }
    } else {
      setUser(null);
    }
    setLoading(false);
  }, [siteConfig.customFields.apiBaseUrl]);

  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  const login = async (token) => {
    localStorage.setItem('access_token', token);
    await fetchUser();
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
    window.location.href = siteConfig.baseUrl; // Redirect to Docusaurus base URL
  };

  const authContextValue = {
    user,
    loading,
    login,
    logout,
    isAuthenticated: !!user,
  };

  return (
    <AuthContext.Provider value={authContextValue}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
