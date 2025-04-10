// Executed when the page loads
document.addEventListener('DOMContentLoaded', () => {
    checkAdminAuth();
    loadUsers();
    setupUserForm();
});

// Checks if the user is an admin
async function checkAdminAuth() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = '/login.html';
        return;
    }

    try {
        const response = await fetch('/api/v1/auth/profile', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const userData = await response.json();

        if (!userData.is_admin) {
            window.location.href = '/';
        }
    } catch (error) {
        console.error('Admin verification error:', error);
        window.location.href = '/login.html';
    }
}

// Sets up the user creation form
function setupUserForm() {
    const form = document.getElementById('create-user-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = {
            email: form.email.value,
            password: form.password.value,
            first_name: form.firstName.value,
            last_name: form.lastName.value,
            is_admin: form.isAdmin.checked
        };

        try {
            const response = await fetch('/api/v1/admin/users', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getCookie('token')}`
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (response.ok) {
                showMessage('User created successfully!', 'success');
                form.reset();
                loadUsers();  // Reload the user list
            } else {
                showMessage(result.error || 'Error during creation', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showMessage('Error while creating the user', 'error');
        }
    });
}

// Loads the list of users
async function loadUsers() {
    try {
        const response = await fetch('/api/v1/admin/users', {
            headers: {
                'Authorization': `Bearer ${getCookie('token')}`
            }
        });

        if (!response.ok) {
            throw new Error('Error loading users');
        }

        const users = await response.json();
        displayUsers(users);
    } catch (error) {
        console.error('Error:', error);
        showMessage('Error while loading users', 'error');
    }
}

// Displays the list of users
function displayUsers(users) {
    const usersList = document.getElementById('users-list');
    usersList.innerHTML = users.map(user => `
        <div class="user-card">
            <div class="user-info">
                <h3>${sanitizeHTML(user.first_name)} ${sanitizeHTML(user.last_name)}</h3>
                <p>${sanitizeHTML(user.email)}</p>
                <p class="user-role">${user.is_admin ? 'Administrator' : 'User'}</p>
            </div>
            <div class="user-actions">
                ${user.is_admin ?
                    `<button onclick="demoteUser('${user.id}')" class="button warning">
                        <span class="icon">⬇️</span> Demote
                    </button>` :
                    `<button onclick="promoteUser('${user.id}')" class="button success">
                        <span class="icon">⬆️</span> Promote
                    </button>`
                }
                <button onclick="deleteUser('${user.id}')" class="button danger">
                    <span class="icon">🗑️</span> Delete
                </button>
            </div>
        </div>
    `).join('');
}

// Promotes a user to admin
async function promoteUser(userId) {
    if (!confirm('Are you sure you want to promote this user to administrator?')) {
        return;
    }

    try {
        const response = await fetch(`/api/v1/admin/users/${userId}/promote`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${getCookie('token')}`
            }
        });

        if (response.ok) {
            showMessage('User promoted successfully', 'success');
            loadUsers();
        } else {
            const data = await response.json();
            showMessage(data.error || 'Error during promotion', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showMessage('Error while promoting the user', 'error');
    }
}

// Demotes an admin to regular user
async function demoteUser(userId) {
    if (!confirm('Are you sure you want to demote this administrator?')) {
        return;
    }

    try {
        const response = await fetch(`/api/v1/admin/users/${userId}/demote`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${getCookie('token')}`
            }
        });

        if (response.ok) {
            showMessage('User demoted successfully', 'success');
            loadUsers();
        } else {
            const data = await response.json();
            showMessage(data.error || 'Error during demotion', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showMessage('Error while demoting the user', 'error');
    }
}

// Deletes a user
async function deleteUser(userId) {
    if (!confirm('Are you sure you want to delete this user?')) {
        return;
    }

    try {
        const response = await fetch(`/api/v1/admin/users/${userId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${getCookie('token')}`
            }
        });

        if (response.ok) {
            showMessage('User deleted successfully', 'success');
            loadUsers();
        } else {
            const data = await response.json();
            showMessage(data.error || 'Error during deletion', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showMessage('Error while deleting the user', 'error');
    }
}

// Displays a notification message
function showMessage(message, type = 'info') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    document.querySelector('main').prepend(messageDiv);

    setTimeout(() => messageDiv.remove(), 5000);
}

// Gets a cookie by its name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Sanitizes strings for HTML display
function sanitizeHTML(str) {
    if (!str) return '';
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

// User logout
function logout() {
    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    window.location.href = '/login.html';
}
