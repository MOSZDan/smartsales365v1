# SmartSales365 Backend - Django REST API

Backend API for SmartSales365 multi-vendor e-commerce platform built with Django REST Framework.

## 📋 Features

- ✅ **JWT Authentication** - Complete auth system with register, login, logout
- ✅ **Password Reset** - Email-based password recovery via MailerSend
- ✅ **User Management** - Profile management and address CRUD
- ✅ **Multi-Vendor** - Store creation and management
- ✅ **Products** - Full product catalog with categories
- ✅ **Orders** - Order processing with multiple statuses
- ✅ **Ratings & Reviews** - Product rating system
- ✅ **Coupons** - Discount code management
- ✅ **PostgreSQL** - Neon database support
- ✅ **API Documentation** - Auto-generated Swagger/OpenAPI docs

## 🛠️ Tech Stack

- **Django 5.0** - Web framework
- **Django REST Framework** - REST API
- **SimpleJWT** - JWT authentication
- **PostgreSQL** - Database (Neon)
- **MailerSend** - Transactional emails
- **drf-spectacular** - API documentation

## 🚀 Quick Start

### Prerequisites

- Python 3.10+ installed
- PostgreSQL database (Neon account)
- MailerSend account with API key

### 1. Setup Virtual Environment

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the `backend/` directory:

```bash
cp .env .env
```

Edit `.env` with your credentials:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Your Neon PostgreSQL URL
DATABASE_URL=postgresql://user:password@your-neon-host.neon.tech:5432/smartsales365

# Frontend URL (for CORS)
CORS_ALLOWED_ORIGINS=http://localhost:3000

# MailerSend
MAILERSEND_API_KEY=mlsn.your-api-key-here
MAILERSEND_SENDER_DOMAIN=your-verified-domain.com
DEFAULT_FROM_EMAIL=noreply@your-verified-domain.com
```

**Generate SECRET_KEY:**

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

Backend will be available at: **http://127.0.0.1:8000/**

## 📚 API Endpoints

### Authentication (`/api/auth/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/register/` | Register new user | No |
| POST | `/login/` | User login | No |
| POST | `/logout/` | User logout | Yes |
| POST | `/token/refresh/` | Refresh JWT token | No |
| GET/PUT | `/profile/` | Get/Update user profile | Yes |
| POST | `/change-password/` | Change password | Yes |
| POST | `/password-reset/` | Request password reset | No |
| POST | `/password-reset-confirm/` | Confirm password reset | No |
| GET/POST | `/addresses/` | List/Create addresses | Yes |
| GET/PUT/DELETE | `/addresses/{id}/` | Address details | Yes |

### Products (`/api/products/`)

> To be implemented with full CRUD operations

### Stores (`/api/stores/`)

> To be implemented with vendor management

### Orders (`/api/orders/`)

> To be implemented with checkout flow

### Ratings (`/api/ratings/`)

> To be implemented with review system

### Coupons (`/api/coupons/`)

> To be implemented with validation

## 📖 API Documentation

Once the server is running, visit:

- **Swagger UI:** http://127.0.0.1:8000/api/docs/
- **OpenAPI Schema:** http://127.0.0.1:8000/api/schema/

## 🔐 Authentication Flow

### 1. Register

```bash
POST /api/auth/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!"
}
```

**Response:**
```json
{
  "user": {
    "id": "uuid-here",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "tokens": {
    "access": "eyJ0eXAiOi...",
    "refresh": "eyJ0eXAiOi..."
  }
}
```

### 2. Login

```bash
POST /api/auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

### 3. Use Access Token

```bash
GET /api/auth/profile/
Authorization: Bearer eyJ0eXAiOi...
```

### 4. Refresh Token

```bash
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOi..."
}
```

### 5. Password Reset

**Step 1:** Request reset email

```bash
POST /api/auth/password-reset/
Content-Type: application/json

{
  "email": "user@example.com"
}
```

User receives email with reset link: `http://localhost:3000/reset-password/{uid}/{token}`

**Step 2:** Confirm reset

```bash
POST /api/auth/password-reset-confirm/
Content-Type: application/json

{
  "uidb64": "MQ",
  "token": "c4r7l9-abc123...",
  "new_password": "NewSecurePass123!",
  "new_password_confirm": "NewSecurePass123!"
}
```

## 🗄️ Database Models

### User
- Custom user model with email authentication
- Fields: id (UUID), email, name, image, cart (JSON)

### Store
- Multi-vendor store management
- Fields: id, userId, name, username, logo, status (pending/approved)

### Product
- Product catalog
- Fields: id, name, description, mrp, price, images (array), category

### Order
- Order processing
- Statuses: ORDER_PLACED, PROCESSING, SHIPPED, DELIVERED
- Payment methods: COD, STRIPE

### OrderItem
- Order line items (junction table)

### Rating
- Product reviews (1-5 stars)

### Address
- User delivery addresses

### Coupon
- Discount codes with expiration

## 🧪 Testing

Run tests with:

```bash
python manage.py test
```

## 📦 Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migrations
python manage.py showmigrations

# Rollback migration
python manage.py migrate app_name migration_name
```

## 🔧 Admin Panel

Access Django admin at: http://127.0.0.1:8000/admin/

Login with your superuser credentials.

## 🐛 Troubleshooting

### Database Connection Error

```
django.db.utils.OperationalError: could not connect to server
```

**Solution:** Check your `DATABASE_URL` in `.env` file. Ensure Neon database is accessible.

### MailerSend Email Not Sending

```
anymail.exceptions.AnymailAPIError
```

**Solution:**
1. Verify `MAILERSEND_API_KEY` is correct
2. Ensure sender domain is verified in MailerSend
3. Check `DEFAULT_FROM_EMAIL` uses verified domain

### Module Not Found

```
ModuleNotFoundError: No module named 'rest_framework'
```

**Solution:** Activate virtual environment and install dependencies:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## 📁 Project Structure

```
backend/
├── apps/
│   ├── users/          # Authentication & user management
│   ├── products/       # Product catalog
│   ├── stores/         # Multi-vendor stores
│   ├── orders/         # Order processing
│   ├── ratings/        # Product reviews
│   └── coupons/        # Discount codes
├── config/
│   ├── settings.py     # Django settings
│   ├── urls.py         # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── templates/
│   └── users/
│       └── password_reset_email.html
├── manage.py
├── requirements.txt
└── .env.example
```

## 🚀 Deployment

### Prepare for Production

1. Set `DEBUG=False` in `.env`
2. Update `ALLOWED_HOSTS` with your domain
3. Set strong `SECRET_KEY`
4. Configure static files:
   ```bash
   python manage.py collectstatic
   ```

### Using Gunicorn

```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## 📝 License

MIT License - See LICENSE.md

## 🤝 Contributing

See CONTRIBUTING.md for contribution guidelines.
