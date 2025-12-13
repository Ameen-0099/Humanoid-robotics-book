export const API_BASE_URL = process.env.NODE_ENV === 'production'
  ? 'https://api.humanoid-robotics-book.com' // Replace with your actual production API URL
  : 'http://localhost:8000'; // Default for development

export const API_AUTH_SIGNUP = `${API_BASE_URL}/auth/signup`;
export const API_AUTH_LOGIN = `${API_BASE_URL}/auth/login`;
export const API_CHATBOT = `${API_BASE_URL}/api/chatbot`;
