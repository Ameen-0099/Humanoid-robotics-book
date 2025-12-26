import express from "express";
// The 'cors' library is replaced by the manual middleware below
import { toNodeHandler } from "better-auth/node";
import { auth } from "./app/better-auth.js";

const app = express();
const port = 8001;

// Global request logger - to confirm requests are reaching Express
app.use((req, res, next) => {
    console.log('Incoming request:', req.method, req.url);
    next();
});

// Manual CORS Middleware to handle pre-flight requests
app.use((req, res, next) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    res.setHeader('Access-Control-Allow-Credentials', 'true');
    // Intercept and approve OPTIONS requests
    if (req.method === 'OPTIONS') {
        return res.sendStatus(204);
    }
    next();
});

app.use(express.json());

app.all("/auth/*", toNodeHandler(auth));


app.listen(port, () => {
    console.log(`Better-Auth server listening on http://localhost:${port}`);
});