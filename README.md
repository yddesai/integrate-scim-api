# SCIM 2.0 API Server

A SCIM 2.0-compliant RESTful API server that supports automated user and group provisioning and deprovisioning. This server is compatible with multiple Identity Providers (IdPs) including Okta, Azure AD, and OneLogin.

## Features

- Full SCIM 2.0 compliance (RFC 7643 and RFC 7644)
- Support for multiple IdPs (Okta, Azure AD, OneLogin)
- User and Group management
- HTTP Basic Authentication and OAuth 2.0 Bearer Token support
- SQLite database for development (configurable for production)
- Comprehensive API documentation
- Extensible architecture

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- virtualenv (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd scim-server
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database:
```bash
flask db upgrade
```

## Configuration

The application can be configured through environment variables or a `.env` file:

- `FLASK_APP`: Application entry point
- `FLASK_ENV`: Environment (development/production)
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Application secret key
- `JWT_SECRET_KEY`: JWT signing key
- `BASIC_AUTH_USERNAME`: Basic auth username
- `BASIC_AUTH_PASSWORD`: Basic auth password

## Running the Server

Development:
```bash
flask run
```

Production:
```bash
gunicorn "app:create_app()"
```

## API Documentation

The API documentation is available at `/docs` when running the server. The following endpoints are implemented:

### Users
- GET /scim/v2/Users
- POST /scim/v2/Users
- GET /scim/v2/Users/{id}
- PUT /scim/v2/Users/{id}
- PATCH /scim/v2/Users/{id}
- DELETE /scim/v2/Users/{id}

### Groups
- GET /scim/v2/Groups
- POST /scim/v2/Groups
- GET /scim/v2/Groups/{id}
- PUT /scim/v2/Groups/{id}
- PATCH /scim/v2/Groups/{id}
- DELETE /scim/v2/Groups/{id}

### Service Provider Configuration
- GET /scim/v2/ServiceProviderConfig
- GET /scim/v2/ResourceTypes
- GET /scim/v2/Schemas

## Testing

Run the test suite:
```bash
pytest
```

## Deployment

The application can be deployed to various platforms:

### Docker
```bash
docker build -t scim-server .
docker run -p 5000:5000 scim-server
```

### Azure App Service
1. Create an Azure App Service
2. Configure deployment from GitHub
3. Set environment variables in Azure Portal

### AWS Elastic Beanstalk
1. Create an Elastic Beanstalk environment
2. Deploy using the AWS CLI or console
3. Configure environment variables

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 