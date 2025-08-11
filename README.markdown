# PollPro - A Comprehensive Polling Management System

Welcome to **PollPro**, a full-featured polling management system built with **Django Rest Framework (DRF)**. PollPro is designed to empower users to create, participate in, and manage polls while providing administrators with a dedicated interface to oversee the entire platform. This project is a robust backend solution that supports a dynamic polling ecosystem, including user authentication, poll creation with expiration dates, vote tracking, and advanced administrative controls. It serves as a scalable foundation for a full-stack application, with plans for future integration with a frontend framework like React or Vue.js.

PollPro is structured into multiple Django apps—`users`, `polls`, and `pollpro_admin`—to modularize functionality and ensure maintainability. Whether you're a user casting votes or an admin managing the system, PollPro offers a secure, efficient, and extensible platform tailored to polling needs.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Running the Project](#running-the-project)
- [Directory Structure](#directory-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Overview
PollPro is a Django-based RESTful API project aimed at creating a polling platform where users can engage with polls across various categories (e.g., Entertainment, Technology, Sports) and administrators can manage the ecosystem. The project is divided into three core apps:

- **users**: Handles user registration, authentication, and profile management using JWT-based security.
- **polls**: Manages poll creation, options, expiration dates, and user voting with real-time tracking.
- **pollpro_admin**: Provides an admin-specific interface and API endpoints for overseeing users, polls, and votes, including CRUD operations and analytics.

This structure allows for clear separation of concerns, making it easy to extend or integrate with a frontend. The project is inspired by the need for a modern, scalable polling system that supports both end-user interaction and administrative oversight, with a focus on security and performance.

## Features
- **User Management (users app)**: Secure registration, login, and profile updates with JWT authentication.
- **Poll Management (polls app)**: Create polls with multiple options, set expiration dates, and track user participation.
- **Vote Tracking (polls app)**: Record and retrieve votes, ensuring one vote per user per poll.
- **Admin Controls (pollpro_admin app)**: Comprehensive dashboard for managing users, polls, and votes, including deletion and updates.
- **RESTful API**: Exposes endpoints for all core functionalities, accessible via DRF's browsable interface.
- **Scalability**: Designed with DRF to support future frontend integrations and large-scale deployments.
- **Security**: Implements token-based authentication, input validation, and role-based access control.

## Tech Stack
- **Backend**: Python 3.11, Django 4.x, Django Rest Framework 3.x
- **Database**: PostgreSQL 15 (or SQLite for development)
- **Authentication**: `djangorestframework-simplejwt` for JWT
- **Dependencies**: `django-cors-headers`, `psycopg2-binary`, `python-decouple`
- **Development Tools**: `pip`, `virtualenv`, `git`

## Prerequisites
- Python 3.11 or higher
- Node.js and npm (optional, for future frontend integration)
- PostgreSQL 15 (or SQLite for local development)
- Git
- A code editor (e.g., VSCode)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/maina2/alx-project-nexus.git
cd pollpro
```

### 2. Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the `.env.example` file to `.env` and update the values:
```bash
cp .env.example .env
```
Edit `.env` with your settings:
- `SECRET_KEY`: Generate a secure Django secret key.
- `DATABASE_URL`: Set your PostgreSQL URL (e.g., `postgres://user:password@localhost:5432/pollpro`).
- `DEBUG`: Set to `True` for development, `False` for production.
- `ALLOWED_HOSTS`: List of allowed hostnames (e.g., `localhost`, `127.0.0.1`).

### 5. Apply Migrations
```bash
python manage.py migrate
```

### 6. Create a Superuser
```bash
python manage.py createsuperuser
```

## Configuration
- **Database**: Uses SQLite by default for development. For production, configure PostgreSQL in `settings.py` or `.env`.
- **CORS**: Update `CORS_ALLOWED_ORIGINS` in `settings.py` if integrating with a frontend.
- **JWT**: Configure token settings in `settings.py` under `SIMPLE_JWT` (e.g., token expiration).

## API Documentation
PollPro provides a RESTful API with endpoints organized by app. Access via DRF's browsable interface or tools like Postman. Use `Authorization: Bearer <token>` for protected routes.

### Authentication (users app)
- **POST /api/token/**: Obtain JWT tokens.
  - Body: `{ "username": "user", "password": "pass" }`
- **POST /api/token/refresh/**: Refresh access token.
  - Body: `{ "refresh": "refresh_token" }`

### Users (users app)
- `GET /api/users/`: List all users (admin only).
- `GET /api/users/{id}/`: Retrieve a user.
- `POST /api/users/`: Register a new user.
- `PUT /api/users/{id}/`: Update user (admin only).
- `DELETE /api/users/{id}/`: Delete user (admin only).

### Polls (polls app)
- `GET /api/polls/`: List all polls.
- `GET /api/polls/{id}/`: Retrieve a poll.
- `POST /api/polls/`: Create a poll (authenticated users).
- `PUT /api/polls/{id}/`: Update a poll (creator or admin).
- `DELETE /api/polls/{id}/`: Delete a poll (creator or admin).

### Votes (polls app)
- `GET /api/votes/`: List all votes (admin only).
- `POST /api/votes/`: Cast a vote.
- `DELETE /api/votes/{id}/`: Remove a vote (admin only).

### Admin (pollpro_admin app)
- `GET /api/admin/users/`: Admin view of users.
- `GET /api/admin/polls/`: Admin view of polls with analytics.
- `GET /api/admin/votes/`: Admin view of votes.
- `POST /api/admin/bulk-delete/`: Bulk delete users/polls/votes (admin only).

## Running the Project
Activate the virtual environment (if not already active).  
Run the development server:
```bash
python manage.py runserver
```
Access the API at [http://localhost:8000/](http://localhost:8000/) or the admin panel at [http://localhost:8000/admin/](http://localhost:8000/admin/).

## Directory Structure
```
pollpro/
├── pollpro/              # Main Django project directory
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/                 # Custom apps
│   ├── users/            # User authentication and profiles
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── polls/            # Poll and vote management
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   └── pollpro_admin/    # Admin-specific controls
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Contributing
We welcome contributions to PollPro! To get started:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`.
3. Commit your changes: `git commit -m "Add your message"`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Submit a pull request.

### Guidelines
- Follow PEP 8 for Python code.
- Write tests for new features using Django’s testing framework.
- Update documentation and API endpoints as needed.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
Author: Simon Maina Chanzu  
Email: chanzusimon6@gmail.com  
GitHub: https://github.com/maina2  
Issues: Report bugs or suggest features at Issues Page
