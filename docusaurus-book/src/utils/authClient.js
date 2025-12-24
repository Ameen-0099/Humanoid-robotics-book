import { createAuthClient } from "better-auth/client";

// Assuming your backend better-auth instance is mounted at /api/auth
export const authClient = createAuthClient({
  baseUrl: "/api/auth", // Relative path, will be proxied by Docusaurus
});
