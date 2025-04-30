## Disclaimer
For more information about this project, please refer to Part 1 README.md, Part 2 README.md and Part 3 README.md!


# HairBedsnBeers (HBnB) - Part 4: Web Client

## Overview
This is the fourth part of the HairBedsnBeers project, focusing on the web client implementation. This web client connects to the RESTful API developed in Part 3 to provide a user-friendly interface for interacting with the HBnB platform.

## Features
- Browse available places
- Filter places by price, city
- View detailed information about places
- User authentication (login/logout)
- Add and view reviews for places
- Responsive design for mobile and desktop

## Prerequisites
- Web server (can be a simple HTTP server)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- The HBnB API server running (from Part 3)

## Project Structure
```
part4/
├── index.html            # Main landing page showing all places
├── login.html            # User login page
├── place.html            # Detailed view for a specific place
├── add_review.html       # Page for adding reviews to a place
├── styles.css            # CSS styles for the application
├── scripts.js            # JavaScript functionality
├── images/               # Images and assets
└── tests/                # Tests for the web client
    └── HBNBv2.postman_collection.json  # Postman collection for testing the API
```

## Running the Web Client

### Method 1: Using Python's built-in HTTP server
1. Navigate to the part4 directory:
   ```
   cd holbertonschool-hbnb-part4/part4
   ```

2. Start a simple HTTP server:
   ```
   # For Python 3
   python -m http.server 8080

   # For Python 2
   python -m SimpleHTTPServer 8080
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:8080
   ```

### Method 2: Using Node.js http-server
1. Install http-server if you haven't already:
   ```
   npm install -g http-server
   ```

2. Navigate to the part4 directory:
   ```
   cd holbertonschool-hbnb-part4/part4
   ```

3. Start the server:
   ```
   http-server -p 8080
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:8080
   ```

### Method 3: Using any other web server
You can use any web server of your choice (Apache, Nginx, etc.) to serve the static files. Just make sure to configure the web server to serve the part4 directory as the root.

## Connecting to the API

By default, the web client is configured to connect to the API at `http://localhost:5000/api/v1`. If your API is running on a different host or port, you need to modify the `API_BASE_URL` constant in `scripts.js`.

To start the API server:
1. Navigate to the part3 directory:
   ```
   cd holbertonschool-hbnb-part3/part3/hbnb
   ```

2. Activate the virtual environment:
   ```
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

4. Run the application:
   ```
   ./setup.sh
   ```

## Testing

### API Testing with Postman
1. Import the Postman collection from `tests/HBNBv2.postman_collection.json`
2. Make sure the API server is running
3. Run the collection in Postman

### Web Client Manual Testing
1. Launch the web client as described above
2. Test the following functionality:
   - Browse places on the homepage
   - Apply filters (price, city, country)
   - View place details by clicking on a place
   - Log in using the admin account (email: admin@example.com, password: admin123)
   - Add a review to a place
   - Log out

## User Accounts for Testing
- Admin users:
  - Email: admin@HairBedsnBeers.com
  - Password: admin123
  - Email: admin@example.com
  - Password: admin123


## Troubleshooting

### CORS Issues
If you encounter CORS (Cross-Origin Resource Sharing) issues, make sure your API server has CORS enabled. In the Part 3 Flask API, this is typically handled by the Flask-CORS extension.

## Browser Compatibility
The web client has been tested and should work properly on:
- Chrome (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Edge (latest 2 versions)

## Credits
- HairBedsnBeers Team
- Holberton School
