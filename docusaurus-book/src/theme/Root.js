import React from 'react';
import { AuthProvider } from '../../src/contexts/AuthContext';

// Default implementation, that you can customize
function Root({ children }) {
  return (
    <AuthProvider>
      {children}
    </AuthProvider>
  );
}

export default Root;