import { betterAuth } from "better-auth";
import { Pool } from "pg";

function initializeAuth() {
  try {
    const connectionString = process.env.NEON_DATABASE_URL;
    const authSecret = process.env.BETTER_AUTH_SECRET;

    // Explicitly check for required environment variables
    if (!connectionString) {
      throw new Error("CRITICAL: NEON_DATABASE_URL environment variable is not set. Please check your .env file.");
    }
    if (!authSecret) {
      throw new Error("CRITICAL: BETTER_AUTH_SECRET environment variable is not set. Please check your .env file.");
    }

    const pool = new Pool({
      connectionString: `${connectionString}?sslmode=require`,
    });

    const authInstance = betterAuth({
      // Add the missing required options
      secret: authSecret,
      baseUrl: "http://localhost:3000", // The URL of your Docusaurus app
      trustedOrigins: ["http://localhost:3000"],

      database: pool,
      emailAndPassword: {
        enabled: true
      },
      additionalFields: {
        softwareBackground: {
          type: "string",
          required: false,
        },
        hardwareBackground: {
          type: "string",
          required: false,
        }
      }
    });

    console.log("✅ 'better-auth' initialized successfully.");
    return authInstance;

  } catch (error) {
    console.error("!!! FAILED TO INITIALIZE AUTHENTICATION !!!");
    console.error("This is likely due to an invalid database connection string or a missing/invalid 'BETTER_AUTH_SECRET'.");
    console.error(error);
    process.exit(1);
  }
}

export const auth = initializeAuth();
