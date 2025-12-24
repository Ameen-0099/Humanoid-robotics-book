export const API_BASE_URL = process.env.NODE_ENV === 'production'
  ? 'https://api.humanoid-robotics-book.com' // Production API URL
  : 'http://localhost:8000'; // Point to fastapi-backend for development/SSR

export const API_AUTH_SIGNUP = 'http://localhost:8001/api/auth/email/signup'; // Point to new Node.js auth service
export const API_AUTH_LOGIN = 'http://localhost:8001/api/auth/email/login'; // Point to new Node.js auth service
export const API_CHATBOT = `${API_BASE_URL}/api/chatbot`;
