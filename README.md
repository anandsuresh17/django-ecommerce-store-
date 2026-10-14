# NOVA – E-Commerce Website

NOVA is a Django-based e-commerce website built with a clean, modern interface and user account management. This project demonstrates full-stack web development using Python, Django, HTML, CSS, and JavaScript.

## Deployment Status

**Status: Deployed and Live**

NOVA is deployed on **Render** and is accessible online.

- **Live Website:** https://django-ecommerce-store-hd0t.onrender.com/
- **Admin Panel:** https://django-ecommerce-store-hd0t.onrender.com/admin/
- **Hosting Platform:** Render

## GitHub Repository

https://github.com/anandsuresh17/django-ecommerce-store-.git

## Technologies Used

- Python
- Django 6.1.2
- HTML5
- CSS3
- JavaScript
- Django Template Language
- Pillow 12.3.0
- python-dotenv 1.2.4
- WhiteNoise

## Database

SQLite (confirm that this matches the database configured for the deployed application).

## Features

### 1. User Authentication
- User registration with personal details.
- Login using email and password.
- Logout functionality.
- Remember Me option for extended login sessions.

### 2. User Profile
- Dedicated profile page for authenticated users.
- Displays registered user information.

### 3. Password Recovery
- Email-based OTP verification.
- OTP expiration and verification attempt limits.
- Password reset with password validation.

### 4. Product Catalog
- Product listings with images, prices, and descriptions.
- Product browsing through the storefront.
- Clean, user-friendly interface.

### 5. Admin Panel
- Django administration interface for managing application data.
- Administrative access for authorized users.

## Project Structure

```text
ecom-proj/
├── account/
│   ├── templates/
│   │   ├── signup.html
│   │   ├── signin.html
│   │   ├── profile.html
│   │   ├── forgot_password.html
│   │   ├── verify_otp.html
│   │   └── new_password.html
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
├── myapp/
├── myproject/
│   ├── settings.py
│   └── urls.py
├── templates/
├── manage.py
└── requirements.txt
```

*The structure shown is representative; the actual repository may differ.*

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/anandsuresh17/django-ecommerce-store-.git
cd ecom-proj
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root and configure the required environment variables, such as the Django secret key and email credentials.

Never commit your `.env` file or sensitive credentials to GitHub.

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

### 6. Create an Admin Account

```bash
python manage.py createsuperuser
```

Follow the prompts to create an administrator account for your local environment.

### 7. Run the Development Server

```bash
python manage.py runserver
```

Open the local website:

http://127.0.0.1:8000/

## Third-Party Libraries

| Library | Purpose |
|---|---|
| Django | Backend framework, routing, authentication, and database integration |
| Pillow | Image handling and processing |
| python-dotenv | Environment variable management |
| WhiteNoise | Static file serving during deployment |
| asgiref | Asynchronous support for the Django ecosystem |
| sqlparse | SQL parsing utility |
| tzdata | Time-zone database support |

## Security

- Store sensitive settings in environment variables.
- Never publish admin passwords, test-user passwords, or email app passwords.
- Use strong, unique passwords for administrative accounts.
- Keep production security settings appropriately configured.

## Author

**Anand Suresh**

GitHub: https://github.com/anandsuresh17

## Project Information

- **Project Name:** NOVA E-Commerce Website
- **Framework:** Django
- **Deployment Platform:** Render
- **Deployment Status:** Live

---

*Developed as a Django e-commerce web development project.*
