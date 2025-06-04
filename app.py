from flask import Flask, request, jsonify, render_template_string
import mysql.connector

app = Flask(__name__)

# Database Configuration
db_config = {
    'host': 'veera.c5awqomecj30.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'Cloud123',
    'database': 'dev'  # Change to your actual database name
}

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(**db_config)

# HTML Frontend Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Management</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f9; }
        h1 { color: #333; }
        .form-container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); max-width: 500px; margin: auto; }
        input, button { padding: 10px; margin: 10px 0; width: 100%; border: 1px solid #ccc; border-radius: 4px; }
        button { background-color: #4CAF50; color: white; cursor: pointer; }
        button:hover { background-color: #45a049; }
        .user-list { margin-top: 20px; }
        .user-item { background: white; padding: 10px; margin: 5px 0; border-radius: 4px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); }
    </style>
</head>
<body>

<h1>User Management</h1>

<!-- Add User Form -->
<div class="form-container">
    <h2>Add New User</h2>
    <input type="text" id="name" placeholder="Name" required />
    <input type="email" id="email" placeholder="Email" required />
    <button onclick="addUser()">Add User</button>
</div>

<!-- Update User Form -->
<div class="form-container" style="margin-top: 30px;">
    <h2>Update User</h2>
    <input type="number" id="userId" placeholder="User ID" required />
    <input type="text" id="newName" placeholder="New Name" required />
    <input type="email" id="newEmail" placeholder="New Email" required />
    <button onclick="updateUser()">Update User</button>
</div>

<!-- User List -->
<div class="user-list">
    <h2>All Users</h2>
    <div id="usersContainer"></div>
</div>

<script>
    // Fetch all users and display them
    function fetchUsers() {
        fetch('/users')
            .then(response => response.json())
            .then(data => {
                const usersContainer = document.getElementById('usersContainer');
                usersContainer.innerHTML = '';  // Clear existing users
                data.forEach(user => {
                    usersContainer.innerHTML += `
                        <div class="user-item">
                            <p><strong>ID:</strong> ${user.id}</p>
                            <p><strong>Name:</strong> ${user.name}</p>
                            <p><strong>Email:</strong> ${user.email}</p>
                            <button onclick="deleteUser(${user.id})">Delete</button>
                        </div>
                    `;
                });
            });
    }

    // Add a new user
    function addUser() {
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;

        fetch('/users/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, email })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || data.error);
            fetchUsers();  // Refresh the user list
        });
    }

    // Update an existing user
    function updateUser() {
        const userId = document.getElementById('userId').value;
        const name = document.getElementById('newName').value;
        const email = document.getElementById('newEmail').value;

        fetch(`/users/update/${userId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, email })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || data.error);
            fetchUsers();  // Refresh the user list
        });
    }

    // Delete a user by ID
    function deleteUser(userId) {
        fetch(`/users/delete/${userId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || data.error);
            fetchUsers();  // Refresh the user list
        });
    }

    // Initialize by fetching users on page load
    window.onload = fetchUsers;
</script>

</body>
</html>
'''

#1️⃣ Get all users
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify(users)

# 2️⃣ Get user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()
    
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

# 3️⃣ Add a new user
@app.route('/users/add', methods=['POST'])
def add_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({'error': 'Name and Email are required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        return jsonify({'message': 'User added successfully'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# 4️⃣ Update user by ID
@app.route('/users/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({'error': 'Name and Email are required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    if not cursor.fetchone():
        return jsonify({'error': 'User not found'}), 404

    try:
        cursor.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, user_id))
        conn.commit()
        return jsonify({'message': 'User updated successfully'})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# 5️⃣ Delete user by ID
@app.route('/users/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    if not cursor.fetchone():
        return jsonify({'error': 'User not found'}), 404

    try:
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        return jsonify({'message': 'User deleted successfully'})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# Serve the HTML page
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
