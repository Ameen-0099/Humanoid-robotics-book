// test_auth_init.ts
// A minimal file to test 'better-auth' initialization in isolation.

import { betterAuth } from "better-auth";
import { Pool } from "pg";

console.log("Starting minimal auth test...");

try {
  const connectionString = process.env.NEON_DATABASE_URL;
  const authSecret = process.env.BETTER_AUTH_SECRET;
  const authServerUrl = process.env.BETTER_AUTH_SERVER_URL;

  if (!connectionString || !authSecret || !authServerUrl) {
    throw new Error(`CRITICAL: One or more environment variables are missing.
      NEON_DATABASE_URL: ${!!connectionString}
      BETTER_AUTH_SECRET: ${!!authSecret}
      BETTER_AUTH_SERVER_URL: ${!!authServerUrl}
    `);
  }

  console.log("Environment variables loaded successfully.");

  const pool = new Pool({
    connectionString: `${connectionString}?sslmode=require`,
  });

  console.log("Database pool created.");

  const authInstance = betterAuth({
    secret: authSecret,
    baseUrl: authServerUrl,
    database: pool,
    emailAndPassword: { enabled: true },
  });

  console.log("✅ SUCCESS: 'better-auth' initialized without crashing.");

} catch (error) {
  console.error("❌ FAILURE: The test script caught an error.");
  console.error(error);
  process.exit(1);
}
