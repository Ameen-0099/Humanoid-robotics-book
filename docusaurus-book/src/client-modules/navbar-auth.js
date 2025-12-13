import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment';

if (ExecutionEnvironment.canUseDOM) {
  // Function to update navbar items based on login status
  const updateNavbarAuthItems = () => {
    const token = localStorage.getItem('token');
    const userString = localStorage.getItem('user'); // Get the user object string
    let loggedInUser = null;

    if (userString) {
      try {
        loggedInUser = JSON.parse(userString); // Parse the user object
      } catch (e) {
        console.error("Failed to parse user data from localStorage", e);
      }
    }

    const loginLink = document.querySelector('.navbar-login-link');
    const signupLink = document.querySelector('.navbar-signup-link');
    const profileLink = document.querySelector('.navbar-profile-link');

    // Check if both token and parsed user object exist
    if (token && loggedInUser && loggedInUser.name) {
      // User is logged in
      if (loginLink) loginLink.style.display = 'none';
      if (signupLink) signupLink.style.display = 'none';
      if (profileLink) {
        profileLink.style.display = 'flex'; // Show profile link
        // Update label with username from the parsed user object
        const profileLabel = profileLink.querySelector('.navbar__link-label');
        if (profileLabel) {
          profileLabel.textContent = loggedInUser.name; // Use loggedInUser.name
        }
      }
    } else {
      // User is logged out
      if (loginLink) loginLink.style.display = 'flex';
      if (signupLink) signupLink.style.display = 'flex';
      if (profileLink) profileLink.style.display = 'none'; // Hide profile link
    }
  };

  // Run on initial load
  updateNavbarAuthItems();

  // Listen for changes in local storage (e.g., login/logout)
  window.addEventListener('storage', updateNavbarAuthItems);

  // Also update when navigating between pages within Docusaurus
  // This might not be strictly necessary if local storage change triggers 'storage' event
  // but good for robustness when history.push is used directly.
  window.addEventListener('popstate', updateNavbarAuthItems); // For browser back/forward
  document.addEventListener('DOMContentLoaded', updateNavbarAuthItems); // For initial load or hard refreshes

  // Add a custom event listener for when login/logout happens within the app
  // This allows explicit triggers if needed, though 'storage' event should cover most cases
  window.addEventListener('authStatusChange', updateNavbarAuthItems);
}
