import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    try {
      const sessionJson = localStorage.getItem('auth_session');
      if (sessionJson) {
        const session = JSON.parse(sessionJson);
        // Assuming the session object from better-auth contains user info.
        // This might need to be adjusted based on the actual session structure.
        // For example, it might be session.user.email
        setUser({ email: session.email || 'user' }); 
      } else {
        setUser(null);
      }
    } catch (error) {
      console.error("Failed to parse auth session", error);
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = () => {
    localStorage.removeItem('auth_session');
    setUser(null);
    window.location.href = '/'; // Redirect to home after logout
  };

  const authContextValue = {
    user,
    loading,
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
