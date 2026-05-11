TASK 4: ROLE-BASED ACCESS CONTROL AND REST API

1. ROLE LOGIC
The application manages different permission levels by using a 'role' column in the 'users' table.
Implementation: The database schema was modified using an ALTER TABLE SQL command to add a role
column with a default value of 'user'.
Session Handling: Upon a successful login, the system retrieves the user's role from the database
and stores it in the Flask session as session['role']. This allows the app to remember
 if the logged-in person is an admin or a standard user throughout their visit.

3. API ENDPOINTS
The project includes a REST API that allows for data exchange in JSON format instead of traditional HTML.
GET /api/students: Fetches and returns a list of all students as a JSON array.
POST /api/students: Allows for adding a new student by sending JSON data to the server.
PUT /api/students/: Used to update existing student records in the database based on their unique ID.

2. SECURITY FLOW
To protect sensitive administrative pages, a custom Python decorator named @admin_required was created.
Function: This decorator acts as a security guard for specific routes.
Validation: When a user tries to access the /admin route, the decorator checks if 'user' 
is in the session and if session['role'] is equal to 'admin'.
Redirection: If the credentials do not match 'admin', the user is automatically redirected to the dashboard,
 preventing unauthorized access to user management tools.

