// Handle login form submission
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            // Get form data
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            // Validate inputs
            if (!email || !password) {
                showMessage('Please enter both email and password', 'error');
                return;
            }

            // Disable submit button to prevent multiple submissions
            const submitButton = loginForm.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            submitButton.innerHTML = '<span class="loading-spinner"></span> Logging in...';

            try {
                // Send login request to API
                const response = await fetch('/api/v1/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();

                if (response.ok) {
                    // Login successful

                    // Store token in cookie
                    document.cookie = `token=${data.token}; path=/; max-age=86400`;

                    // Show success message
                    showMessage('Login successful! Redirecting...', 'success');

                    // Redirect to home page after a short delay
                    setTimeout(() => {
                        window.location.href = '/';
                    }, 1500);
                } else {
                    // Login failed
                    showMessage(data.error || 'Login failed. Please check your credentials.', 'error');
                    submitButton.disabled = false;
                    submitButton.innerHTML = 'Login';
                }
            } catch (error) {
                console.error('Error during login:', error);
                showMessage('An error occurred during login. Please try again.', 'error');
                submitButton.disabled = false;
                submitButton.innerHTML = 'Login';
            }
        });
    }

    // Check if user is already logged in
    checkAuthentication();
});

// Check if user is already authenticated
function checkAuthentication() {
    const token = getCookie('token');

    if (token) {
        // User is already logged in, redirect to home page
        window.location.href = '/';
    }
}

// Show a notification message
function showMessage(message, type = 'info') {
    const messageContainer = document.createElement('div');
    messageContainer.className = `message ${type}`;
    messageContainer.textContent = message;

    document.body.appendChild(messageContainer);

    // Remove message after 5 seconds
    setTimeout(() => {
        messageContainer.classList.add('fade-out');
        setTimeout(() => {
            document.body.removeChild(messageContainer);
        }, 500);
    }, 5000);
}

// Get a cookie by name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Registration handler
document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const button = e.target.querySelector('button[type="submit"]');
    const spinner = button.querySelector('.loading-spinner');

    // Disable the button and show the spinner
    button.disabled = true;
    spinner.style.display = 'inline-block';

    try {
        const formData = {
            email: document.getElementById('reg-email').value,
            password: document.getElementById('reg-password').value,
            first_name: document.getElementById('reg-firstName').value,
            last_name: document.getElementById('reg-lastName').value,
            is_admin: false  // Always false for new users
        };

        const response = await fetch('/api/v1/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (response.ok) {
            // Automatically log in the user
            document.cookie = `token=${data.token}; path=/`;
            window.location.href = '/';
        } else {
            showError(data.error || 'Error during registration', 'register-form');
            button.disabled = false;
            spinner.style.display = 'none';
        }
    } catch (error) {
        console.error('Error:', error);
        showError('An error occurred during registration', 'register-form');
        button.disabled = false;
        spinner.style.display = 'none';
    }
});

// Display an error message
function showError(message, formId) {
    // Remove old errors
    const oldError = document.querySelector(`#${formId} + .error-message`);
    if (oldError) {
        oldError.remove();
    }

    // Create and display the new error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `
        <span class="icon">⚠️</span>
        ${message}
    `;

    // Insert error after the form
    const form = document.getElementById(formId);
    form.parentNode.insertBefore(errorDiv, form.nextSibling);

    // Automatically remove the error after 5 seconds
    setTimeout(() => {
        errorDiv.style.opacity = '0';
        setTimeout(() => errorDiv.remove(), 300);
    }, 5000);
}
