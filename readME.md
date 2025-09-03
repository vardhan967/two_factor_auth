# Two-Factor Authentication System (2FA)

A secure and modern two-factor authentication system built with **Django** & **Django REST Framework**.  
This project implements **JWT authentication** with an additional **OTP-based verification via email**.  
It demonstrates best practices in authentication workflows, environment variable management, and secure API development for real-world applications.

---

## Badges
- ![Django](https://img.shields.io/badge/Django-4.2-green)
- ![DRF](https://img.shields.io/badge/Django%20REST%20Framework-API-red)
- ![JWT](https://img.shields.io/badge/Auth-JWT-blue)
- ![2FA](https://img.shields.io/badge/Security-2FA-orange)
- ![License: MIT](https://img.shields.io/badge/License-MIT-yellow)

---

## Features
- ✅ User Registration & Login with JWT Authentication  
- ✅ Two-Factor Authentication (2FA) using Email OTP  
- ✅ OTP resend functionality  
- ✅ Secure handling of secrets & environment variables  
- ✅ REST API designed with Django REST Framework  
- ✅ CORS-enabled for frontend integration  
- ✅ SQLite (local dev) with support for PostgreSQL/MySQL  
- ✅ Ready for deployment on cloud (Heroku, Render, AWS, etc.)  

---

## Tech Stack
- **Backend:** Django, Django REST Framework  
- **Authentication:** JWT + Email OTP (2FA)  
- **Database:** SQLite (default), PostgreSQL/MySQL (optional)  
- **Email Service:** Gmail SMTP (demo) — can be replaced with SendGrid, AWS SES, etc.  
- **Tools:** Python, pip, virtualenv  
- **Environment:** dotenv (`.env`) for secrets  

---

## Project Structure
```
two_factor_auth/
│── accounts/        # Authentication & OTP app
│── two_factor_auth/ # Project settings & configurations
│── db.sqlite3       # Default SQLite database (local dev)
│── requirements.txt # Python dependencies
│── manage.py        # Django project manager
```

---

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/vardhan967/two_factor_auth.git
   cd two_factor_auth
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Mac/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create `.env` file**
   ```env
   DJANGO_SECRET_KEY=your-secret-key
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

6. **Run migrations**
   ```bash
   python manage.py migrate
   ```

7. **Start the server**
   ```bash
   python manage.py runserver
   ```

➡ App runs at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## API Endpoints

| Endpoint           | Method | Description                |
|--------------------|--------|----------------------------|
| `/api/register/`   | POST   | Register new user          |
| `/api/login/`      | POST   | Login with username/password |
| `/api/verify-otp/` | POST   | Verify OTP after login     |
| `/api/resend-otp/` | POST   | Resend a new OTP           |

**Example Request:**
```http
POST /api/login/
Content-Type: application/json

{
  "username": "john",
  "password": "securepassword"
}
```

---

## Why This Project?

- 🔐 Demonstrates secure authentication workflows used in production apps.  
- 🔑 Implements two-factor authentication with OTP verification.  
- 📦 Shows proficiency in Django REST Framework, JWT, and environment management.  
- ☁️ Designed for scalability and cloud deployment.  
- 💼 Great for showcasing security-focused backend development skills to recruiters.  

---

## License
This project is licensed under the **MIT License**.

---

## Author

**Satya Prakash Vardhan**  
- 💻 Backend Developer | Python | Django  
- 📧 [satyaprakashvardhan@gmail.com](mailto:satyaprakashvardhan@gmail.com)  
- 🔗 [LinkedIn](https://www.linkedin.com/in/your-profile)  
- 🐙 [GitHub](https://github.com/vardhan967)  
- 🌐 [Portfolio](https://your-portfolio-link.com)  
