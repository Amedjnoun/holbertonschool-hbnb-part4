/**
 * HairBedsnBeers Web Client
 * Main JavaScript file handling all client-side functionality
 */

// Global constants and configuration
const API_BASE_URL = 'http://localhost:5000/api/v1'; // Change this to your API URL
const TOKEN_COOKIE_NAME = 'hbnb_auth_token';
const TIMEOUT_MS = 10000; // 10 seconds timeout for API calls

// Cache for API responses to reduce server load
const apiCache = new Map();

/**
 * Initialization function - runs when DOM is fully loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    // Determine which page we're on and initialize accordingly
    const currentPath = window.location.pathname;
    const pageName = currentPath.split('/').pop();

    // Update navigation based on authentication status
    updateNavigation();

    // Initialize the appropriate page
    if (pageName === 'index.html' || pageName === '') {
        initHomePage();
    } else if (pageName === 'login.html') {
        initLoginPage();
    } else if (pageName === 'place.html') {
        initPlaceDetailsPage();
    } else if (pageName === 'add_review.html') {
        initAddReviewPage();
    }
});

/**
 * Updates navigation links based on user authentication status
 */
function updateNavigation() {
    const token = getCookie(TOKEN_COOKIE_NAME);
    const loginLink = document.getElementById('login-link');

    if (loginLink) {
        if (token) {
            // User is logged in, show logout button
            loginLink.textContent = 'Logout';
            loginLink.href = '#';
            loginLink.addEventListener('click', function(e) {
                e.preventDefault();
                logout();
            });
        } else {
            // User is not logged in, show login button
            loginLink.textContent = 'Login';
            loginLink.href = 'login.html';

            // Remove any existing click event listeners
            const newLoginLink = loginLink.cloneNode(true);
            loginLink.parentNode.replaceChild(newLoginLink, loginLink);
        }
    }
}

/**
 * Initializes the home page with places and filters
 */
function initHomePage() {
    // Get filter elements
    const priceFilter = document.getElementById('price-filter');
    const countryFilter = document.getElementById('country-filter');
    const cityFilter = document.getElementById('city-filter');
    const applyFiltersBtn = document.getElementById('apply-filters');
    const clearFiltersBtn = document.getElementById('clear-filters');
    const loadingIndicator = document.getElementById('loading-indicator');
    const placesContainer = document.getElementById('places-container');
    const placesError = document.getElementById('places-error');

    // Load places from API
    fetchPlaces()
        .then(places => {
            // Hide loading indicator
            if (loadingIndicator) loadingIndicator.style.display = 'none';

            // Populate filters
            populatePriceFilter(places);
            populateCountryFilter(places);
            populateCityFilter(places);

            // Display places
            displayPlaces(places);

            // Initialize filter functionality
            if (applyFiltersBtn) {
                applyFiltersBtn.addEventListener('click', function() {
                    const maxPrice = priceFilter ? priceFilter.value : '999999';
                    const country = countryFilter ? countryFilter.value : 'all';
                    const city = cityFilter ? cityFilter.value : 'all';

                    // Filter places
                    const filteredPlaces = filterPlaces(places, maxPrice, country, city);

                    // Update display
                    displayPlaces(filteredPlaces);
                    updateFilterSummary(maxPrice, country, city, filteredPlaces.length);
                });
            }

            if (clearFiltersBtn) {
                clearFiltersBtn.addEventListener('click', function() {
                    // Reset filters
                    if (priceFilter) priceFilter.value = '999999';
                    if (countryFilter) countryFilter.value = 'all';
                    if (cityFilter) cityFilter.value = 'all';

                    // Show all places
                    displayPlaces(places);
                    updateFilterSummary('999999', 'all', 'all', places.length);
                });
            }
        })
        .catch(error => {
            // Hide loading indicator
            if (loadingIndicator) loadingIndicator.style.display = 'none';

            // Show error message
            if (placesError) {
                placesError.textContent = `Error loading places: ${error.message}`;
                placesError.style.display = 'block';
            }
            console.error('Error fetching places:', error);
        });
}

/**
 * Populates the price filter with options from the places data
 * @param {Array} places - Array of place objects
 */
function populatePriceFilter(places) {
    const priceFilter = document.getElementById('price-filter');
    if (!priceFilter) return;

    // Clear existing options
    priceFilter.innerHTML = '';

    // Add "All" option
    const allOption = document.createElement('option');
    allOption.value = '999999'; // Very high value to include all
    allOption.textContent = 'All';
    priceFilter.appendChild(allOption);

    // Get unique prices and sort them
    const prices = [...new Set(places.map(place => place.price))].sort((a, b) => a - b);

    // Add an option for each price
    prices.forEach(price => {
        const option = document.createElement('option');
        option.value = price;
        option.textContent = `$${price}`;
        priceFilter.appendChild(option);
    });
}

/**
 * Populates the country filter with options from the places data
 * @param {Array} places - Array of place objects
 */
function populateCountryFilter(places) {
    const countryFilter = document.getElementById('country-filter');
    if (!countryFilter) return;

    // Clear existing options
    countryFilter.innerHTML = '';

    // Add "All" option
    const allOption = document.createElement('option');
    allOption.value = 'all';
    allOption.textContent = 'All Countries';
    countryFilter.appendChild(allOption);

    // Get unique countries and sort them
    const countries = [...new Set(places.map(place => place.country))].sort();

    // Add an option for each country
    countries.forEach(country => {
        const option = document.createElement('option');
        option.value = country;
        option.textContent = country;
        countryFilter.appendChild(option);
    });
}

/**
 * Populates the city filter with options from the places data
 * @param {Array} places - Array of place objects
 */
function populateCityFilter(places) {
    const cityFilter = document.getElementById('city-filter');
    if (!cityFilter) return;

    // Clear existing options
    cityFilter.innerHTML = '';

    // Add "All" option
    const allOption = document.createElement('option');
    allOption.value = 'all';
    allOption.textContent = 'All cities';
    cityFilter.appendChild(allOption);

    // Get unique cities and sort them
    const cities = [...new Set(places.filter(place => place.city).map(place => place.city))].sort();

    // Add an option for each city
    cities.forEach(city => {
        if (city) {  // Ensure city isn't null or undefined
            const option = document.createElement('option');
            option.value = city;
            option.textContent = city;
            cityFilter.appendChild(option);
        }
    });
}

/**
 * Filters places based on maximum price, country, and city
 * @param {Array} places - Array of place objects
 * @param {string} maxPrice - Maximum price to filter by
 * @param {string} country - Country to filter by
 * @param {string} city - City to filter by
 * @returns {Array} - Filtered array of place objects
 */
function filterPlaces(places, maxPrice, country, city) {
    return places.filter(place => {
        const priceMatch = place.price <= maxPrice;
        const countryMatch = country === 'all' || place.country === country;
        const cityMatch = city === 'all' || place.city === city;
        return priceMatch && countryMatch && cityMatch;
    });
}

/**
 * Updates the filter summary text
 * @param {string} maxPrice - Selected maximum price
 * @param {string} country - Selected country
 * @param {string} city - Selected city
 * @param {number} count - Number of places after filtering
 */
function updateFilterSummary(maxPrice, country, city, count) {
    const summaryElement = document.getElementById('filter-summary');
    if (!summaryElement) return;

    let summaryText = '';

    if (maxPrice === '999999' && country === 'all' && city === 'all') {
        summaryText = `Showing all ${count} available places`;
    } else {
        const priceText = maxPrice === '999999' ? 'any price' : `up to $${maxPrice}`;
        const countryText = country === 'all' ? 'any country' : country;
        const cityText = city === 'all' ? 'any city' : city;
        summaryText = `Showing ${count} place${count !== 1 ? 's' : ''} with ${priceText} in ${countryText}, ${cityText}`;
    }

    summaryElement.textContent = summaryText;
}

/**
 * Displays places in the UI
 * @param {Array} places - Array of place objects to display
 */
function displayPlaces(places) {
    const container = document.getElementById('places-container');
    if (!container) return;

    // Clear existing content
    container.innerHTML = '';

    if (places.length === 0) {
        // Show no results message
        const emptyState = document.createElement('div');
        emptyState.className = 'empty-state';
        emptyState.innerHTML = `
            <p>No places found matching your criteria</p>
            <button id="reset-filters" class="btn-secondary">Reset Filters</button>
        `;
        container.appendChild(emptyState);

        // Add event listener to reset button
        const resetBtn = emptyState.querySelector('#reset-filters');
        if (resetBtn) {
            resetBtn.addEventListener('click', function() {
                const clearFiltersBtn = document.getElementById('clear-filters');
                if (clearFiltersBtn) clearFiltersBtn.click();
            });
        }

        return;
    }

    // Create and append place cards
    places.forEach(place => {
        const placeCard = createPlaceCard(place);
        container.appendChild(placeCard);
    });
}

/**
 * Creates a place card element
 * @param {Object} place - Place object
 * @returns {HTMLElement} - Place card element
 */
function createPlaceCard(place) {
    const li = document.createElement('li');
    li.className = 'place-card';

    // Use a placeholder image since none is provided in the API
    const imageUrl = place.image_url || 'images/placeholder.jpg';

    // Using the API's format (title and price) instead of name and price_by_night
    li.innerHTML = `
        <img src="${imageUrl}" alt="${place.title}" class="place-card-img">
        <div class="place-card-content">
            <h3 class="place-card-title">${place.title}</h3>
            <p class="place-card-price">$${place.price} per night</p>
            <p class="place-card-location">${place.city || 'Location not specified'}, ${place.country || 'Country not specified'}</p>
            <p class="place-card-description">${place.description ? truncateText(place.description, 100) : 'No description available'}</p>
            <a href="place.html?id=${place.id}" class="place-card-link">View Details</a>
        </div>
    `;

    return li;
}

/**
 * Initializes the login page
 */
function initLoginPage() {
    // If user is already logged in, redirect to home page
    const token = getCookie(TOKEN_COOKIE_NAME);
    if (token) {
        window.location.href = 'index.html';
        return;
    }

    const loginForm = document.getElementById('login-form');
    const errorMessage = document.getElementById('login-error');

    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // Clear previous error
            if (errorMessage) {
                errorMessage.style.display = 'none';
                errorMessage.textContent = '';
            }

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            // Validate inputs
            if (!email || !password) {
                if (errorMessage) {
                    errorMessage.textContent = 'Please enter both email and password.';
                    errorMessage.style.display = 'block';
                }
                return;
            }

            // Disable form during submission
            const submitButton = loginForm.querySelector('button[type="submit"]');
            if (submitButton) submitButton.disabled = true;

            // Attempt login
            login(email, password)
                .then(response => {
                    // Set auth token in cookie
                    setCookie(TOKEN_COOKIE_NAME, response.token, 7);

                    // Redirect to home page
                    window.location.href = 'index.html';
                })
                .catch(error => {
                    // Show error message
                    if (errorMessage) {
                        errorMessage.textContent = error.message || 'Login failed. Please check your credentials.';
                        errorMessage.style.display = 'block';
                    }
                    console.error('Login error:', error);
                })
                .finally(() => {
                    // Re-enable form
                    if (submitButton) submitButton.disabled = false;
                });
        });
    }
}

/**
 * Initializes the place details page
 */
function initPlaceDetailsPage() {
    // Get place ID from URL
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');

    if (!placeId) {
        // No place ID provided, redirect to home page
        window.location.href = 'index.html';
        return;
    }

    const token = getCookie(TOKEN_COOKIE_NAME);
    const addReviewSection = document.getElementById('add-review');

    // Hide or show add review section based on auth status
    if (addReviewSection) {
        addReviewSection.style.display = token ? 'block' : 'none';
    }

    // Load place details
    fetchPlaceDetails(placeId)
        .then(place => {
            // Update page title
            document.title = `${place.title} - HairBedsnBeers`;

            // Update place details
            updatePlaceDetails(place);

            // Load reviews for this place
            return fetchReviews(placeId);
        })
        .then(reviews => {
            // Display reviews
            displayReviews(reviews);
        })
        .catch(error => {
            console.error('Error loading place details:', error);

            // Show error message
            const container = document.querySelector('.place-info');
            if (container) {
                container.innerHTML = `
                    <h3>Error</h3>
                    <p>Failed to load place details: ${error.message}</p>
                    <a href="index.html" class="btn-secondary">Return to Home</a>
                `;
            }
        });

    // Setup review form if it exists
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        // Character counter for review text
        const reviewText = document.getElementById('review-text');
        const charCount = document.getElementById('char-count');

        if (reviewText && charCount) {
            reviewText.addEventListener('input', function() {
                const count = this.value.length;
                charCount.textContent = `${count}/1000`;

                // Add warning class if approaching limit
                if (count > 900) {
                    charCount.classList.add('warning');
                } else {
                    charCount.classList.remove('warning');
                }
            });
        }

        // Form submission
        reviewForm.addEventListener('submit', function(e) {
            e.preventDefault();

            if (!token) {
                // Not logged in, redirect to login page
                window.location.href = 'login.html';
                return;
            }

            const reviewContent = reviewText ? reviewText.value : '';

            // Validate input
            if (!reviewContent || reviewContent.trim().length < 10) {
                const errorElement = document.getElementById('review-error');
                if (errorElement) {
                    errorElement.textContent = 'Please enter a review with at least 10 characters.';
                    errorElement.style.display = 'block';
                }
                return;
            }

            // Disable form during submission
            const submitButton = reviewForm.querySelector('button[type="submit"]');
            if (submitButton) submitButton.disabled = true;

            // Submit review
            submitReview(placeId, reviewContent)
                .then(() => {
                    // Reload reviews
                    return fetchReviews(placeId);
                })
                .then(reviews => {
                    // Display updated reviews
                    displayReviews(reviews);

                    // Clear form
                    if (reviewText) reviewText.value = '';
                    if (charCount) charCount.textContent = '0/1000';

                    // Hide error message if visible
                    const errorElement = document.getElementById('review-error');
                    if (errorElement) errorElement.style.display = 'none';
                })
                .catch(error => {
                    // Show error message
                    const errorElement = document.getElementById('review-error');
                    if (errorElement) {
                        errorElement.textContent = `Failed to submit review: ${error.message}`;
                        errorElement.style.display = 'block';
                    }
                    console.error('Error submitting review:', error);
                })
                .finally(() => {
                    // Re-enable form
                    if (submitButton) submitButton.disabled = false;
                });
        });
    }
}

/**
 * Updates the place details in the UI
 * @param {Object} place - Place object
 */
function updatePlaceDetails(place) {
    // Update place name
    const nameElement = document.querySelector('.place-info h3');
    if (nameElement) nameElement.textContent = place.title;

    // Update other details
    const ownerElement = document.getElementById('place-owner');
    if (ownerElement) ownerElement.textContent = place.owner_name || 'Unknown';

    const priceElement = document.getElementById('place-price');
    if (priceElement) priceElement.textContent = `$${place.price}`;

    const descriptionElement = document.getElementById('place-description');
    if (descriptionElement) descriptionElement.textContent = place.description || 'No description available';

    const amenitiesElement = document.getElementById('place-amenities');
    if (amenitiesElement) {
        // Fetch amenities for this place
        fetchAmenities(place.id)
            .then(amenities => {
                if (amenities && amenities.length > 0) {
                    // Map the amenities to their names and join them with commas
                    const amenityNames = amenities.map(amenity => amenity.name);
                    amenitiesElement.textContent = amenityNames.join(', ');
                } else {
                    amenitiesElement.textContent = 'None listed';
                }
            })
            .catch(error => {
                console.error('Error loading amenities:', error);
                amenitiesElement.textContent = 'Failed to load amenities';
            });
    }
}

/**
 * Displays reviews in the UI
 * @param {Array} reviews - Array of review objects
 */
function displayReviews(reviews) {
    const container = document.querySelector('.reviews-list');
    if (!container) return;

    // Clear existing content
    container.innerHTML = '';

    if (reviews.length === 0) {
        container.innerHTML = '<p>No reviews yet. Be the first to leave a review!</p>';
        return;
    }

    // Create and append review cards
    reviews.forEach(review => {
        const reviewCard = createReviewCard(review);
        container.appendChild(reviewCard);
    });
}

/**
 * Creates a review card element
 * @param {Object} review - Review object
 * @returns {HTMLElement} - Review card element
 */
function createReviewCard(review) {
    const div = document.createElement('div');
    div.className = 'review-card';

    // Format the date properly
    let formattedDate = 'Unknown date';
    if (review.created_at) {
        try {
            // Try various date formats that might come from the API
            const date = new Date(review.created_at);

            // Check if date is valid
            if (!isNaN(date.getTime())) {
                const options = {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                };
                formattedDate = date.toLocaleDateString(undefined, options);
            }
        } catch (e) {
            console.error('Error formatting date:', e);
            formattedDate = 'Unknown date';
        }
    }

    div.innerHTML = `
        <p class="review-content">${review.text}</p>
        <p class="review-author">- ${review.user_name || 'Anonymous'}</p>
        <p class="review-date">${formattedDate}</p>
    `;

    return div;
}

/**
 * Initializes the add review page
 */
function initAddReviewPage() {
    // Get place ID from URL
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');

    // Check if user is logged in
    const token = getCookie(TOKEN_COOKIE_NAME);

    if (!token) {
        // Not logged in, redirect to login page
        window.location.href = 'login.html';
        return;
    }

    if (!placeId) {
        // No place ID provided, redirect to home page
        window.location.href = 'index.html';
        return;
    }

    // Load place details to show place name
    fetchPlaceDetails(placeId)
        .then(place => {
            // Update place name
            const nameElement = document.getElementById('place-name');
            if (nameElement) nameElement.textContent = place.title;
        })
        .catch(error => {
            console.error('Error loading place details:', error);
        });

    // Character counter for review comment
    const reviewComment = document.getElementById('review-comment');
    const charCount = document.getElementById('char-count');

    if (reviewComment && charCount) {
        reviewComment.addEventListener('input', function() {
            const count = this.value.length;
            charCount.textContent = `${count}/1000`;

            // Add warning class if approaching limit
            if (count > 900) {
                charCount.classList.add('warning');
            } else {
                charCount.classList.remove('warning');
            }
        });
    }

    // Form submission
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const comment = reviewComment ? reviewComment.value : '';
            const ratingElement = document.getElementById('rating');
            const rating = ratingElement ? ratingElement.value : '5';

            // Validate input
            if (!comment || comment.trim().length < 10) {
                const errorElement = document.getElementById('review-error');
                if (errorElement) {
                    errorElement.textContent = 'Please enter a review with at least 10 characters.';
                    errorElement.style.display = 'block';
                }
                return;
            }

            // Disable form during submission
            const submitButton = reviewForm.querySelector('button[type="submit"]');
            if (submitButton) submitButton.disabled = true;

            // Submit review
            submitReview(placeId, comment, rating)
                .then(() => {
                    // Redirect to place details page
                    window.location.href = `place.html?id=${placeId}`;
                })
                .catch(error => {
                    // Show error message
                    const errorElement = document.getElementById('review-error');
                    if (errorElement) {
                        errorElement.textContent = `Failed to submit review: ${error.message}`;
                        errorElement.style.display = 'block';
                    }
                    console.error('Error submitting review:', error);

                    // Re-enable form
                    if (submitButton) submitButton.disabled = false;
                });
        });
    }

    // Cancel button
    const cancelButton = document.getElementById('cancel-review');
    if (cancelButton) {
        cancelButton.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = `place.html?id=${placeId}`;
        });
    }
}

/**
 * API Functions
 */

/**
 * Fetches all places from the API
 * @returns {Promise<Array>} - Promise resolving to array of place objects
 */
async function fetchPlaces() {
    // Check cache first
    if (apiCache.has('places')) {
        return apiCache.get('places');
    }

    try {
        const response = await fetchWithTimeout(`${API_BASE_URL}/places`);

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const places = await response.json();

        // Cache the response
        apiCache.set('places', places);

        return places;
    } catch (error) {
        console.error('Error fetching places:', error);
        throw new Error('Failed to load places. Please try again later.');
    }
}

/**
 * Fetches details for a specific place
 * @param {string} placeId - ID of the place to fetch
 * @returns {Promise<Object>} - Promise resolving to place object
 */
async function fetchPlaceDetails(placeId) {
    // Check cache first
    const cacheKey = `place_${placeId}`;
    if (apiCache.has(cacheKey)) {
        return apiCache.get(cacheKey);
    }

    try {
        const response = await fetchWithTimeout(`${API_BASE_URL}/places/${placeId}`);

        if (!response.ok) {
            // Handle specific error cases
            if (response.status === 404) {
                throw new Error('Place not found. It may have been removed.');
            }
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const place = await response.json();

        // Extract owner information if it's included in the response
        if (place.owner) {
            place.owner_name = `${place.owner.first_name} ${place.owner.last_name}`;
        }

        // Cache the response
        apiCache.set(cacheKey, place);

        return place;
    } catch (error) {
        console.error(`Error fetching place ${placeId}:`, error);
        throw new Error('Failed to load place details. Please try again later.');
    }
}

/**
 * Fetches reviews for a specific place
 * @param {string} placeId - ID of the place to fetch reviews for
 * @returns {Promise<Array>} - Promise resolving to array of review objects
 */
async function fetchReviews(placeId) {
    // Check cache first
    const cacheKey = `reviews_${placeId}`;

    // For reviews, we don't use cache to ensure we always get the latest
    try {
        const response = await fetchWithTimeout(`${API_BASE_URL}/places/${placeId}/reviews`);

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const reviews = await response.json();

        // Fetch user details for each review if needed
        const reviewsWithUserDetails = await Promise.all(reviews.map(async (review) => {
            if (review.user_id && !review.user_name) {
                try {
                    const userResponse = await fetchWithTimeout(`${API_BASE_URL}/users/${review.user_id}`);
                    if (userResponse.ok) {
                        const user = await userResponse.json();
                        review.user_name = `${user.first_name} ${user.last_name}`;
                    }
                } catch (error) {
                    console.error(`Error fetching user for review ${review.id}:`, error);
                    // Don't fail the whole request if we can't get user info
                    review.user_name = "Anonymous";
                }
            }
            return review;
        }));

        return reviewsWithUserDetails;
    } catch (error) {
        console.error(`Error fetching reviews for place ${placeId}:`, error);
        throw new Error('Failed to load reviews. Please try again later.');
    }
}

/**
 * Fetches amenities for a specific place
 * @param {string} placeId - ID of the place to fetch amenities for
 * @returns {Promise<Array>} - Promise resolving to array of amenity objects
 */
async function fetchAmenities(placeId) {
    try {
        const response = await fetchWithTimeout(`${API_BASE_URL}/places/${placeId}/amenities`);

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const amenities = await response.json();
        return amenities;
    } catch (error) {
        console.error(`Error fetching amenities for place ${placeId}:`, error);
        return []; // Return empty array on error to avoid breaking the UI
    }
}

/**
 * Submits a login request to the API
 * @param {string} email - User email
 * @param {string} password - User password
 * @returns {Promise<Object>} - Promise resolving to response object with token
 */
async function login(email, password) {
    try {
        const response = await fetchWithTimeout(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (!response.ok) {
            // Handle specific error cases
            if (response.status === 401) {
                throw new Error('Invalid email or password.');
            }
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Login error:', error);

        // Handle network errors
        if (error.name === 'AbortError') {
            throw new Error('Login request timed out. Please try again.');
        }

        if (error.name === 'TypeError' && error.message.includes('NetworkError')) {
            throw new Error('Network error. Please check your connection and try again.');
        }

        throw error;
    }
}

/**
 * Submits a review for a place
 * @param {string} placeId - ID of the place to review
 * @param {string} text - Review text
 * @param {string} rating - Optional rating value
 * @returns {Promise<Object>} - Promise resolving to response object
 */
async function submitReview(placeId, text, rating = '5') {
    const token = getCookie(TOKEN_COOKIE_NAME);

    if (!token) {
        throw new Error('You must be logged in to submit a review.');
    }

    try {
        const response = await fetchWithTimeout(`${API_BASE_URL}/places/${placeId}/reviews`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                text,
                rating: parseInt(rating, 10)
            })
        });

        if (!response.ok) {
            // Parse error response if available
            const errorData = await response.json().catch(() => null);

            // Handle specific error cases
            if (response.status === 401) {
                throw new Error('Your session has expired. Please log in again.');
            }

            if (response.status === 400) {
                throw new Error(errorData?.error || 'Invalid review data. Please check your input.');
            }

            throw new Error(errorData?.error || `HTTP error! Status: ${response.status}`);
        }

        // Clear the reviews cache for this place to ensure fresh data
        apiCache.delete(`reviews_${placeId}`);

        return await response.json();
    } catch (error) {
        console.error('Submit review error:', error);

        // Handle network errors
        if (error.name === 'AbortError') {
            throw new Error('Request timed out. Please try again.');
        }

        if (error.name === 'TypeError' && error.message.includes('NetworkError')) {
            throw new Error('Network error. Please check your connection and try again.');
        }

        throw error;
    }
}

/**
 * Logs out the current user by clearing the auth token
 */
function logout() {
    // Clear auth token
    deleteCookie(TOKEN_COOKIE_NAME);

    // Clear API cache
    apiCache.clear();

    // Update navigation
    updateNavigation();

    // Redirect to home page
    window.location.href = 'index.html';
}

/**
 * Utility Functions
 */

/**
 * Sets a cookie with the given name, value, and expiration days
 * @param {string} name - Cookie name
 * @param {string} value - Cookie value
 * @param {number} days - Number of days until expiration
 */
function setCookie(name, value, days) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    const expires = `expires=${date.toUTCString()}`;
    document.cookie = `${name}=${value};${expires};path=/;SameSite=Strict`;
}

/**
 * Gets a cookie value by name
 * @param {string} name - Cookie name
 * @returns {string|null} - Cookie value or null if not found
 */
function getCookie(name) {
    const nameEQ = `${name}=`;
    const cookies = document.cookie.split(';');

    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i];
        while (cookie.charAt(0) === ' ') {
            cookie = cookie.substring(1, cookie.length);
        }
        if (cookie.indexOf(nameEQ) === 0) {
            return cookie.substring(nameEQ.length, cookie.length);
        }
    }

    return null;
}

/**
 * Deletes a cookie by name
 * @param {string} name - Cookie name
 */
function deleteCookie(name) {
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;SameSite=Strict`;
}

/**
 * Truncates text to a specified length with ellipsis
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length before truncation
 * @returns {string} - Truncated text
 */
function truncateText(text, maxLength) {
    if (!text || text.length <= maxLength) {
        return text;
    }

    return text.substring(0, maxLength) + '...';
}

/**
 * Fetches a URL with a timeout
 * @param {string} url - URL to fetch
 * @param {Object} options - Fetch options
 * @returns {Promise<Response>} - Promise resolving to fetch response
 */
async function fetchWithTimeout(url, options = {}) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), TIMEOUT_MS);

    try {
        const response = await fetch(url, {
            ...options,
            signal: controller.signal
        });

        clearTimeout(timeoutId);
        return response;
    } catch (error) {
        clearTimeout(timeoutId);
        throw error;
    }
}