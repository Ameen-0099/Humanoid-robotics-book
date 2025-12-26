import { betterAuth } from "better-auth";
import { Pool } from "pg";

console.log('--- Loading better-auth.ts ---');

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
    console.log('--- Database pool created ---');

    pool.on('connect', () => {
      console.log('🐘 Database pool connected');
    });
    
    pool.on('error', (err) => {
      console.error('🔥 Database pool error', err);
    });

    pool.query('SELECT NOW()', (err, res) => {
      if (err) {
        console.error('🔥 Database query error on startup', err);
      } else {
        console.log('🐘 Database query successful on startup:', res.rows[0]);
      }
    });

    const authInstance = betterAuth({
      // Add the missing required options
      secret: authSecret,
      baseUrl: "http://localhost:8001", // The URL of your Docusaurus app
      trustedOrigins: ["http://localhost:3000", "http://localhost:8001"],

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
