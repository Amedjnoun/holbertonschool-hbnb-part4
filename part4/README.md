# HBnB - Rental Application 🏠

## Description
HBnB is a web application for managing property rentals, allowing users to publish and book accommodations, as well as leave reviews.

## Features
- 👥 User management and authentication
- 🏘️ Publishing and managing properties
- ⭐ Review and rating system
- 🛠️ Administration interface
- 🔍 Property search and filtering
- 📅 Booking system
  - Booking validation by the owner
  - Automatic hiding of properties during confirmed booking periods
  - Clear indication of "Reserved from [date] to [date]" on the property page
  - Real-time availability management

## Installation

1. Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
python setup_db.py
```

4. Create the administrator:
```bash
python create_admin.py
```

5. Launch the application:
```bash
python run.py
```

## Project Structure
```
part4/
├── app/                    # Backend code
│   ├── api/               # API routes
│   ├── models/           # Data models
│   └── extensions.py     # Flask extensions
├── static/               # Frontend
│   ├── css/             # Styles by page
│   ├── js/             # JavaScript scripts
│   ├── images/         # Images
│   └── *.html          # HTML pages
└── config.py           # Configuration
```

## Administrator Account
```
Email: admin@hbnb.io
Password: admin12345
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` : Login
- `GET /api/v1/auth/profile` : User profile

### Administration
- `GET /api/v1/admin/users` : List of users
- `POST /api/v1/admin/users` : User creation
- `POST /api/v1/admin/users/<id>/promote` : Admin promotion
- `POST /api/v1/admin/users/<id>/demote` : Admin demotion

### Properties
- `GET /api/v1/places` : List of properties
- `POST /api/v1/places` : Property creation
- `GET /api/v1/places/<id>` : Property details
- `PUT /api/v1/places/<id>` : Property modification
- `DELETE /api/v1/places/<id>` : Property deletion

### Reviews
- `GET /api/v1/places/<id>/reviews` : Property reviews
- `POST /api/v1/places/<id>/reviews` : Review creation

### Bookings
- `POST /api/v1/places/<id>/bookings` : Booking request
- `GET /api/v1/places/<id>/bookings` : List of bookings for a property
- `PUT /api/v1/bookings/<id>/validate` : Booking validation by the owner
- `PUT /api/v1/bookings/<id>/cancel` : Booking cancellation
- `GET /api/v1/users/bookings` : List of user's bookings


## Frontend Pages

- `/` : Homepage with property list
- `/login.html` : Login page
- `/admin.html` : Administration interface
- `/place.html` : Property details with booking system
- `/create-place.html` : Property creation
- `/bookings.html` : Booking management (owner/tenant)

## Technologies Used

- **Backend** :
  - Flask (Web framework)
  - SQLAlchemy (ORM)
  - JWT (Authentication)
  - SQLite (Database)

- **Frontend** :
  - HTML5/CSS3
  - JavaScript (Vanilla)
  - Responsive Design

## Security

- JWT Authentication
- CSRF Protection
- Data validation
- Password hashing
- XSS Protection

## Development

To reset the database:
```bash
python setup_db.py --reset
```

## Notes
- The application uses SQLite in development
- DEBUG mode is enabled by default
- Static files are served directly by Flask

## Author
[Your Name] - 2025
