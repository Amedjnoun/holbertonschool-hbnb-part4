// Wait for DOM to be loaded
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');

    if (placeId) {
        loadPlaceDetails(placeId);
        loadReviews(placeId);
    } else {
        window.location.href = '/';
    }
});

// Check if user is logged in
function checkAuth() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const createPlaceLink = document.getElementById('create-place-link');
    const logoutButton = document.getElementById('logout-button');
    const reviewForm = document.getElementById('review-form');
    const bookingSection = document.getElementById('booking-section');

    if (token) {
        if (loginLink) loginLink.style.display = 'none';
        if (createPlaceLink) createPlaceLink.style.display = 'block';
        if (logoutButton) {
            logoutButton.style.display = 'block';
            logoutButton.addEventListener('click', logout);
        }
        if (reviewForm || bookingSection) {
            fetch('/api/v1/auth/profile', {
                headers: { 'Authorization': `Bearer ${token}` }
            })
            .then(response => response.json())
            .then(data => {
                const urlParams = new URLSearchParams(window.location.search);
                const placeId = urlParams.get('id');
                loadPlace(placeId, data.id, reviewForm, bookingSection);
            });
        }
    } else {
        if (loginLink) loginLink.style.display = 'block';
        if (createPlaceLink) createPlaceLink.style.display = 'none';
        if (logoutButton) logoutButton.style.display = 'none';
        if (reviewForm) reviewForm.style.display = 'none';
        if (bookingSection) bookingSection.style.display = 'none';
    }
}

async function loadPlace(placeId, userId, reviewForm, bookingSection) {
    try {
        const token = getCookie('token');
        // For places, we don't need a token as it's public
        const response = await fetch(`/api/v1/places/${placeId}`);
        const place = await response.json();

        if (!token) {
            // If not logged in, hide interactive sections
            if (reviewForm) reviewForm.style.display = 'none';
            if (bookingSection) bookingSection.style.display = 'none';
            return;
        }

        // Get bookings with token
        const bookingsResponse = await fetch(`/api/v1/places/${placeId}/bookings`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!bookingsResponse.ok) {
            throw new Error('Failed to fetch bookings');
        }

        const bookings = await bookingsResponse.json();

        // If owner
        if (place.owner.id === userId) {
            if (reviewForm) reviewForm.style.display = 'none';
            if (bookingSection) bookingSection.style.display = 'none';
            loadBookings(placeId, bookings);
        } else {
            if (reviewForm) reviewForm.style.display = 'block';
            if (bookingSection) {
                bookingSection.style.display = 'block';
                // Initialize calendar with place and bookings
                initBookingForm(placeId, place, bookings.filter(b => b.status === 'confirmed'));
            }
        }

        // Display booked periods for all users
        displayBookedPeriods(bookings.filter(b => b.status === 'confirmed'));
    } catch (error) {
        console.error('Error:', error);
        if (error.message === 'Failed to fetch bookings') {
            showError('Error retrieving bookings');
        }
    }
}

// Return icon corresponding to amenity
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

// Generate dates to disable in calendar
function generateDisabledDates(bookedPeriods) {
    const disabledDates = [];

    bookedPeriods.forEach(period => {
        if (period.status === 'confirmed') {
            let current = new Date(period.start_date);
            const end = new Date(period.end_date);

            while (current <= end) {
                disabledDates.push(new Date(current));
                current.setDate(current.getDate() + 1);
            }
        }
    });

    return disabledDates;
}

// Check if date range is available
function isDateRangeAvailable(start, end, bookedPeriods) {
    const startDate = new Date(start);
    const endDate = new Date(end);

    return !bookedPeriods.some(period => {
        if (period.status !== 'confirmed') return false;

        const bookedStart = new Date(period.start_date);
        const bookedEnd = new Date(period.end_date);

        return (startDate <= bookedEnd && endDate >= bookedStart);
    });
}

// Function to load place details
async function loadPlaceDetails(placeId) {
    try {
        const token = getCookie('token');
        let userId = null;

        // Get user profile if logged in
        if (token) {
            try {
                const profileResponse = await fetch('/api/v1/auth/profile', {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (profileResponse.ok) {
                    const profile = await profileResponse.json();
                    userId = profile.id;
                }
            } catch (error) {
                console.error('Error fetching profile:', error);
            }
        }

        // Get place details and confirmed bookings
        const [placeResponse, bookingsResponse] = await Promise.all([
            fetch(`/api/v1/places/${placeId}`),
            token ? fetch(`/api/v1/places/${placeId}/bookings`, {
                headers: { 'Authorization': `Bearer ${token}` }
            }) : Promise.resolve(null)
        ]);

        if (!placeResponse.ok) {
            throw new Error('Failed to load place details');
        }

        const place = await placeResponse.json();
        let confirmedBookings = [];

        if (bookingsResponse && bookingsResponse.ok) {
            const bookings = await bookingsResponse.json();
            confirmedBookings = bookings.filter(b => b.status === 'confirmed');
        }

        // Render place details
        const placeDetails = document.getElementById('place-details');
        const priceFormatted = new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'EUR'
        }).format(place.price);

        // Photos handling
        const photosHtml = place.photos && place.photos.length > 0
            ? `
                <div class="place-images-grid">
                    <div class="place-image-main">
                        <img src="${sanitizeHTML(place.photos[0].photo_url)}" alt="Main photo" class="gallery-img">
                    </div>
                    ${place.photos.slice(1).map(photo => `
                        <div class="place-image-item">
                            <img src="${sanitizeHTML(photo.photo_url)}" alt="${sanitizeHTML(photo.caption || '')}" class="gallery-img">
                        </div>
                    `).join('')}
                </div>
            `
            : `
                <div class="place-image-container">
                    <div class="place-image-placeholder">🏠</div>
                </div>
            `;

        placeDetails.innerHTML = `
            ${photosHtml}
            <div class="place-content">
                <h1>${sanitizeHTML(place.title)}</h1>
                <p class="place-location">
                    <span class="icon">📍</span>
                    Latitude: ${place.latitude}, Longitude: ${place.longitude}
                </p>
                <p class="place-price">${priceFormatted} / night</p>
                <div class="place-description">
                    ${sanitizeHTML(place.description || 'No description available.')}
                </div>
                <div class="place-owner">
                    <p><strong>Owner:</strong> ${sanitizeHTML(place.owner.first_name)} ${sanitizeHTML(place.owner.last_name)}</p>
                </div>
                ${place.amenities && place.amenities.length > 0 ? `
                    <div class="place-amenities">
                        <h3>Amenities</h3>
                        <ul>
                            ${place.amenities.map(amenity => `
                                <li>
                                    <span class="amenity-icon">${getAmenityIcon(amenity.name)}</span>
                                    ${sanitizeHTML(amenity.name)}
                                </li>
                            `).join('')}
                        </ul>
                    </div>
                ` : ''}
            </div>
        `;

        // Display bookings or calendar based on user role
        if (userId && place.owner.id === userId) {
            loadBookings(placeId);
            const bookingSection = document.getElementById('booking-section');
            if (bookingSection) bookingSection.style.display = 'none';
        } else {
            const bookingSection = document.getElementById('booking-section');
            if (bookingSection) {
                bookingSection.style.display = 'block';
                initBookingForm(placeId, place, confirmedBookings);
            }
        }

        // Always display booked periods for everyone
        displayBookedPeriods(confirmedBookings);

    } catch (error) {
        console.error('Error loading place details:', error);
        showError('Error loading place details');
    }
}

// Initialize the booking form
function displayBookedPeriods(bookings) {
    const periodsContainer = document.getElementById('booked-periods');
    if (!periodsContainer || !bookings || bookings.length === 0) return;

    periodsContainer.innerHTML = `
        <h3>Booked periods</h3>
        <ul class="booked-periods-list">
            ${bookings.map(booking => `
                <li class="booked-period">
                    <span class="icon">📅</span>
                    From ${new Date(booking.start_date).toLocaleDateString('en-US')}
                    to ${new Date(booking.end_date).toLocaleDateString('en-US')}
                </li>
            `).join('')}
        </ul>
    `;
}

function initBookingForm(placeId, place, confirmedBookings = []) {
    const form = document.getElementById('booking-form');
    if (!form) return;

    // Convert dates to local time for comparison
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const disabledRanges = [];
    const bookedRanges = [];

    confirmedBookings.forEach(booking => {
        const from = new Date(booking.start_date);
        const to = new Date(booking.end_date);
        from.setHours(0, 0, 0, 0);
        to.setHours(0, 0, 0, 0);

        if (to >= today) {
            disabledRanges.push({ from, to });
            bookedRanges.push({ start: from, end: to });
        }
    });

    // Custom calendar styling with status indicators
    const customCalendarConfig = {
        mode: "range",
        dateFormat: "Y-m-d",
        enableTime: false,
        minDate: today,
        altInput: true,
        altFormat: "d F Y",
        locale: {
            firstDayOfWeek: 1,
            weekdays: {
                shorthand: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
                longhand: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
            },
            months: {
                shorthand: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                longhand: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            }
        },
        disable: disabledRanges,
        noCalendar: false,
        disableMobile: false,
        onDayCreate: function(dObj, dStr, fp, dayElem) {
            const date = new Date(dObj);
            const today = new Date();
            today.setHours(0, 0, 0, 0);

            // Colorize calendar days based on status
            const currentDate = new Date(dObj);
            currentDate.setHours(0, 0, 0, 0);

            if (currentDate < today) {
                dayElem.classList.add('past-date');
                dayElem.title = 'Past date';
                return;
            }

            const isBooked = bookedRanges.some(range =>
                currentDate >= range.start && currentDate <= range.end
            );

            if (isBooked) {
                dayElem.classList.add('booked-date');
                dayElem.title = 'Already booked';
                dayElem.innerHTML += '<span class="booked-indicator">•</span>';
            } else {
                dayElem.classList.add('available-date');
                dayElem.title = 'Available';
            }
        },
        onChange: function(selectedDates) {
            if (selectedDates.length === 2) {
                const [start, end] = selectedDates;
                start.setHours(0, 0, 0, 0);
                end.setHours(0, 0, 0, 0);

                // Check for overlaps with booked dates
                const hasOverlap = bookedRanges.some(range => {
                    return (start <= range.end && end >= range.start);
                });

                if (hasOverlap) {
                    showError('These dates are already booked');
                    calendar.clear();
                    document.querySelector('.booking-total').innerHTML = '';
                    return;
                }

                // Calculate and display total
                const nights = Math.ceil((end - start) / (1000 * 60 * 60 * 24));
                const total = nights * place.price;
                document.querySelector('.booking-total').innerHTML = `
                    <p>Duration: ${nights} night${nights > 1 ? 's' : ''}</p>
                    <p>Total: ${new Intl.NumberFormat('en-US', {
                        style: 'currency',
                        currency: 'EUR'
                    }).format(total)}</p>
                `;
            } else {
                document.querySelector('.booking-total').innerHTML = '';
            }
        }
    };

    // Initialize calendar
    const calendar = flatpickr("#booking-dates", customCalendarConfig);

    // Update booking form handler
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const token = getCookie('token');
        if (!token) {
            window.location.href = '/login.html';
            return;
        }

        const button = form.querySelector('button[type="submit"]');
        const spinner = button.querySelector('.loading-spinner');
        button.disabled = true;
        spinner.style.display = 'inline-block';

        try {
            const dates = calendar.selectedDates;
            if (dates.length !== 2) {
                showError('Please select a complete period');
                return;
            }

            const response = await fetch(`/api/v1/places/${placeId}/bookings`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    start_date: dates[0].toISOString().split('T')[0],
                    end_date: dates[1].toISOString().split('T')[0],
                    message: document.getElementById('message').value
                })
            });

            const result = await response.json();

            if (response.ok) {
                form.reset();
                showSuccess('Your booking request has been sent');
                calendar.clear();

                // Reload the page to refresh bookings
                setTimeout(() => window.location.reload(), 2000);
            } else {
                showError(result.error || 'Error during booking');
            }
        } catch (error) {
            console.error('Error creating booking:', error);
            showError('Error during booking');
        } finally {
            button.disabled = false;
            spinner.style.display = 'none';
        }
    });

    // Show booking calendar immediately
    const calendarElem = document.getElementById('booking-dates');
    if (calendarElem) {
        calendarElem.style.display = 'block';
    }
}

// Load bookings for the owner
async function loadBookings(placeId) {
    try {
        const bookingsList = document.getElementById('bookings-list');
        const placeBookings = document.getElementById('place-bookings');
        if (!bookingsList || !placeBookings) return;

        const token = getCookie('token');
        const response = await fetch(`/api/v1/places/${placeId}/bookings`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) {
            throw new Error('Error loading bookings');
        }

        const bookings = await response.json();

        if (bookings.length > 0) {
            placeBookings.style.display = 'block';
            bookingsList.innerHTML = bookings.map(booking => `
                <div class="booking-card ${booking.status}">
                    <div class="booking-header">
                        <span class="booking-user">${sanitizeHTML(booking.user.first_name)} ${sanitizeHTML(booking.user.last_name)}</span>
                        <span class="booking-status">
                            ${booking.status === 'pending' ? 'Pending' :
                              booking.status === 'confirmed' ? 'Confirmed' :
                              booking.status === 'cancelled' ? 'Rejected' : booking.status}
                        </span>
                    </div>
                    <div class="booking-dates">
                        From ${new Date(booking.start_date).toLocaleDateString('en-US')}
                        to ${new Date(booking.end_date).toLocaleDateString('en-US')}
                    </div>
                    ${booking.message ? `
                        <div class="booking-message">
                            ${sanitizeHTML(booking.message)}
                        </div>
                    ` : ''}
                    ${booking.status === 'pending' ? `
                        <div class="booking-actions">
                            <button onclick="updateBooking('${booking.id}', 'confirm')" class="button success">
                                <span class="icon">✅</span> Approve
                            </button>
                            <button onclick="updateBooking('${booking.id}', 'reject')" class="button danger">
                                <span class="icon">❌</span> Reject
                            </button>
                        </div>
                    ` : ''}
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading bookings:', error);
    }
}

// Update a booking status
async function updateBooking(bookingId, action) {
    try {
        const token = getCookie('token');
        if (!token) {
            showError('You must be logged in to perform this action');
            return;
        }

        // Get current placeId from URL
        const urlParams = new URLSearchParams(window.location.search);
        const placeId = urlParams.get('id');

        // Use action-specific endpoints
        const response = await fetch(`/api/v1/places/${placeId}/bookings/${bookingId}/${action}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Failed to update booking');
        }

        const message = action === 'confirm' ? 'approved' : 'rejected';
        showSuccess(`Booking ${message} successfully`);

        // Reload the page to update calendar and bookings
        setTimeout(() => {
            window.location.reload();
        }, 1500);

    } catch (error) {
        console.error('Error updating booking:', error);
        showError(error.message || 'Error updating booking');
    }
}

async function loadReviews(placeId) {
    try {
        const response = await fetch(`/api/v1/places/${placeId}/reviews`);
        const reviews = await response.json();

        const reviewsList = document.getElementById('reviews-list');
        if (reviews.length === 0) {
            reviewsList.innerHTML = '<p>No reviews yet.</p>';
            return;
        }

        reviewsList.innerHTML = reviews.map(review => `
            <div class="review-card">
                <div class="review-header">
                    <span class="review-author">${sanitizeHTML(review.user.first_name)} ${sanitizeHTML(review.user.last_name)}</span>
                    <span class="review-rating">
                        ${'⭐'.repeat(review.rating)}
                    </span>
                </div>
                <p class="review-text">${sanitizeHTML(review.text)}</p>
                <div class="review-date">
                    ${new Date(review.created_at).toLocaleDateString('en-US')}
                </div>
            </div>
        `).join('');

    } catch (error) {
        console.error('Error loading reviews:', error);
        showError('Failed to load reviews');
    }
}

// Review form handling
document.getElementById('add-review-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const token = getCookie('token');
    if (!token) {
        window.location.href = '/login.html';
        return;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');
    const rating = document.getElementById('rating').value;
    const text = document.getElementById('text').value;

    try {
        const response = await fetch(`/api/v1/places/${placeId}/reviews`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ rating: parseInt(rating), text })
        });

        if (response.ok) {
            document.getElementById('rating').value = '';
            document.getElementById('text').value = '';
            loadReviews(placeId);
        } else {
            const data = await response.json();
            showError(data.error || 'Failed to submit review');
        }
    } catch (error) {
        console.error('Error submitting review:', error);
        showError('Failed to submit review');
    }
});

function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.innerHTML = `
        <span class="icon">✅</span>
        ${message}
    `;
    document.querySelector('main').prepend(successDiv);
    setTimeout(() => successDiv.remove(), 5000);
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `
        <span class="icon">⚠️</span>
        ${message}
    `;
    document.querySelector('main').prepend(errorDiv);
    setTimeout(() => errorDiv.remove(), 5000);
}

function sanitizeHTML(str) {
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function logout() {
    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    window.location.href = '/login.html';
}
