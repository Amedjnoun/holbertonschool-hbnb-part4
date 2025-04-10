// Wait for DOM to be loaded
document.addEventListener('DOMContentLoaded', async () => {
    await checkAuth();
    await loadAmenities();
    initPhotoManagement();
});

// Check if user is logged in
async function checkAuth() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = '/login.html';
        return;
    }
}

// Load the list of available amenities
async function loadAmenities() {
    try {
        const response = await fetch('/api/v1/amenities');
        const amenities = await response.json();

        const amenitiesList = document.getElementById('amenities-list');
        // Clear existing list
        amenitiesList.innerHTML = '';

        // Create checkboxes for each amenity
        amenities.forEach(amenity => {
            const amenityIcon = getAmenityIcon(amenity.name);
            const label = document.createElement('label');
            label.className = 'amenity-item';
            label.innerHTML = `
                <input type="checkbox" name="amenities" value="${amenity.id}">
                <span class="amenity-icon">${amenityIcon}</span> ${amenity.name}
            `;
            amenitiesList.appendChild(label);
        });
    } catch (error) {
        console.error('Error loading amenities:', error);
        showError('Error loading amenities');
    }
}

// Return the icon corresponding to the amenity
function getAmenityIcon(name) {
    const icons = {
        'WiFi': '📶',
        'Air conditioning': '❄️',
        'Heating': '🔥',
        'Kitchen': '🍳',
        'TV': '📺',
        'Free parking': '🅿️',
        'Washing machine': '🧺',
        'Swimming pool': '🏊‍♂️',
        'Hot tub': '🌊',
        'Gym': '🏋️‍♂️'
    };
    return icons[name] || '✨';
}

// Initialize photo management
function initPhotoManagement() {
    const addPhotoButton = document.getElementById('add-photo');
    addPhotoButton.addEventListener('click', addPhotoField);

    // Add event handlers for existing delete buttons
    document.querySelectorAll('.remove-photo').forEach(button => {
        button.addEventListener('click', () => removePhotoField(button));
    });
}

// Add a new photo field
function addPhotoField() {
    const photosContainer = document.querySelector('.photos-container');
    const photoDiv = document.createElement('div');
    photoDiv.className = 'photo-upload';

    const isFirstPhoto = document.querySelectorAll('.photo-upload').length === 0;

    photoDiv.innerHTML = `
        <input type="text" placeholder="Photo URL" class="photo-url">
        <input type="text" placeholder="Caption (optional)" class="photo-caption">
        <label class="primary-photo">
            <input type="radio" name="primary-photo" ${isFirstPhoto ? 'checked' : ''}>
            Main photo
        </label>
        <button type="button" class="remove-photo">🗑️</button>
    `;

    // Insert before the add button
    photosContainer.insertBefore(photoDiv, document.getElementById('add-photo'));

    // Add event handler for the delete button
    const removeButton = photoDiv.querySelector('.remove-photo');
    removeButton.addEventListener('click', () => removePhotoField(removeButton));
}

// Remove a photo field
function removePhotoField(button) {
    const photoDiv = button.closest('.photo-upload');
    const wasChecked = photoDiv.querySelector('input[type="radio"]').checked;

    photoDiv.remove();

    // If it was the main photo and there are still photos, select the first one
    if (wasChecked) {
        const firstRadio = document.querySelector('input[type="radio"][name="primary-photo"]');
        if (firstRadio) {
            firstRadio.checked = true;
        }
    }
}

// Get photos from the form
function getPhotos() {
    const photos = [];
    document.querySelectorAll('.photo-upload').forEach(photoDiv => {
        const url = photoDiv.querySelector('.photo-url').value.trim();
        if (url) {
            photos.push({
                photo_url: url,
                caption: photoDiv.querySelector('.photo-caption').value.trim(),
                is_primary: photoDiv.querySelector('input[type="radio"]').checked
            });
        }
    });
    return photos;
}

// Get selected amenities
function getSelectedAmenities() {
    const amenities = [];
    document.querySelectorAll('input[name="amenities"]:checked').forEach(checkbox => {
        amenities.push(checkbox.value);
    });
    return amenities;
}

// Creation form handling
document.getElementById('create-place-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const button = e.target.querySelector('button[type="submit"]');
    const spinner = button.querySelector('.loading-spinner');

    // Disable button and show spinner
    button.disabled = true;
    spinner.style.display = 'inline-block';

    try {
        // Check if at least one photo is provided
        const photos = getPhotos();
        const amenities = getSelectedAmenities();

        // Create object with form data
        const formData = {
            title: document.getElementById('title').value,
            description: document.getElementById('description').value,
            latitude: parseFloat(document.getElementById('latitude').value),
            longitude: parseFloat(document.getElementById('longitude').value),
            price: parseInt(document.getElementById('price').value),
            amenities: amenities,
            photos: photos
        };

        // Coordinate validation
        if (formData.latitude < -90 || formData.latitude > 90) {
            throw new Error('Latitude must be between -90 and 90 degrees');
        }
        if (formData.longitude < -180 || formData.longitude > 180) {
            throw new Error('Longitude must be between -180 and 180 degrees');
        }

        // Send request
        const response = await fetch('/api/v1/places', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getCookie('token')}`
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (response.ok) {
            // Redirect to the created place page
            window.location.href = `/place.html?id=${result.id}`;
        } else {
            showError(result.error || 'Error creating place');
            button.disabled = false;
            spinner.style.display = 'none';
        }
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'An error occurred');
        button.disabled = false;
        spinner.style.display = 'none';
    }
});

// Display an error message
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `
        <span class="icon">⚠️</span>
        ${message}
    `;

    const form = document.getElementById('create-place-form');
    const existingError = form.parentNode.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    form.parentNode.insertBefore(errorDiv, form);

    setTimeout(() => {
        errorDiv.style.opacity = '0';
        setTimeout(() => errorDiv.remove(), 300);
    }, 5000);
}

// Get a cookie by its name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}
