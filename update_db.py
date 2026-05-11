import sqlite3

# Connect to your database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

try:
    # This adds the 'role' column and makes everyone a 'user' by default
    cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
    print("Step 1a: Role column added successfully!")
except sqlite3.OperationalError:
    print("Step 1a: Role column already exists, moving to next part.")

# This makes YOUR specific account the Admin so you can access the secret pages
# REPLACE 'YourUsername' with the username you use to login!
cursor.execute("UPDATE users SET role = 'admin' WHERE username = 'InternUser'")

conn.commit()
conn.close()
print("Step 1b: You are now an Admin. Database is ready!")