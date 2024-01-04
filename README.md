
User Registration and Login: 
Users can register for an account and log in using their credentials.

Caching for User Sessions:
User sessions are cached(redis) to provide a quick and efficient authentication process.

Automatic Session Expiry: 
Sessions expire automatically if the time since the last activity exceeds 300 seconds. This ensures that inactive sessions are cleared for security reasons.
