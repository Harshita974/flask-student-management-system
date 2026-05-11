Task 5 - Web Application Deployment and Cloud Hosting
1. Deployment Steps

Repository Integration: Connected the GitHub repository to the cloud hosting platform 
for automated deployment.

Server Setup: Configured a production-grade WSGI server (Gunicorn) to handle web requests.

Database Initialization: Implemented Python logic to automatically generate the SQLite
schema upon the first server boot.

Optimization: Streamlined the environment by removing local development dependencies
 to ensure a stable build.

2. Environment Variables Used

SFCRFT_KFY: A secure, encrypted string used by the Flask framework to sign session cookies
 and protect user login data.

PORT: Defined as 10000 (default) to route external web traffic to the internal application service.

3. Live URL

Application Link: https://flask-student-management-system-6vrr.onrender.com/login

4. Core Functionalities

Admin Access: Secure gateway for registration and authentication.

CRUD Management: Live interface for adding, viewing, and updating student records.

Session Security: Persistent state tracking for logged-in users.