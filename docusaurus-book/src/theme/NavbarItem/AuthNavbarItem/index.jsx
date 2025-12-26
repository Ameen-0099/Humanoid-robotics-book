import React from 'react';
import { useHistory } from '@docusaurus/router';
import useBaseUrl from '@docusaurus/useBaseUrl';
import { useAuth } from '../../../contexts/AuthContext';
import DropdownNavbarItem from '@theme/NavbarItem/DropdownNavbarItem';
import DefaultNavbarItem from '@theme/NavbarItem/DefaultNavbarItem';


function AuthNavbarItem({ position, className }) {
  const { isAuthenticated, user, logout, loading } = useAuth();
  const history = useHistory();
  const loginUrl = useBaseUrl('/login');
  const signupUrl = useBaseUrl('/signup');
  const profileUrl = useBaseUrl('/profile');

  if (loading) {
    return <DefaultNavbarItem label="Loading..." position={position} className={className} />;
  }

  if (isAuthenticated) {
    const userLabel = user?.email || 'Profile';
    return (
      <DropdownNavbarItem
        label={userLabel}
        position={position}
        className={className}
        items={[
          {
            label: 'My Profile',
            onClick: () => history.push(profileUrl),
          },
          {
            type: 'html',
            value: '<hr class="dropdown-separator">',
          },
          {
            label: 'Logout',
            onClick: () => {
              logout();
              history.push('/');
            },
          },
        ]}
      />
    );
  }

  return (
    <DropdownNavbarItem
      label="Account"
      position={position}
      className={className}
      items={[
        {
          label: 'Login',
          onClick: () => history.push(loginUrl),
        },
        {
          label: 'Sign Up',
          onClick: () => history.push(signupUrl),
        },
      ]}
    />
  );
}

export default AuthNavbarItem;
