# 🚗 ParkKaro - Smart Parking Management System

![Django Version](https://img.shields.io/badge/Django-5.0.6-092E20?style=for-the-badge&logo=django)
![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

ParkKaro is a modern, enterprise-grade, service-oriented smart parking application built using **Django 5.0.6**. It offers real-time booking tracking, location browsing, and automated reservation management. The front-end is designed with premium glassmorphism styling, clean micro-animations, responsive structures, and an AI-powered conversational assistant powered by Google Gemini.


---

## 🌟 Key Features

*   **🔒 Premium Authentication:** Secure user sign-up and login utilizing a customized `User` model with phone verification.
*   **🗺️ Explore & Filter Locations:** Browse active parking sites categorized by venue type (Malls, Hotels, Colleges, Offices) with responsive grid cards.
*   **⚡ Real-Time Active Reservation Tracker:** A dynamic dashboard panel with countdown timers, QR code tickets, and instant slot extensions or cancellations.
*   **💬 ParkBot AI Chatbot:** An integrated conversational agent powered by Google Gemini API to assist users with reservation queries, rates, and help in real-time.
*   **🛠️ Robust Redirection & UX Flow:** Intelligent redirections using HTTP referring headers that keep users within their operational flow (e.g., staying on the dashboard after action completions).
*   **🍃 Fully Responsive Redesigned Footer:** A high-end 4-column footer layout with back-to-top navigation, glassmorphic newsletter subscription form, and social media icons with micro-animations.

---

## 📂 Project Structure

Below is the directory structure of the **ParkKaro** project:

```text
Parking-Management-System-main/
│
├── config/                      # Project Configuration & Settings
│   ├── settings.py              # Main configurations (SQLite, static assets, WhiteNoise)
│   ├── urls.py                  # Core routing definitions
│   ├── wsgi.py / asgi.py        # WSGI and ASGI entry points
│   └── __init__.py
│
├── accounts/                    # User Authentication Application
│   ├── models.py                # Custom User model (extending AbstractUser with 'phone')
│   ├── views.py                 # Login and Register controllers
│   ├── urls.py                  # Account-related URL patterns
│   └── admin.py / apps.py
│
├── parking/                     # Core Business Logic Application
│   ├── models.py                # Database models (Location, ParkingSlot, Booking)
│   ├── views.py                 # Controllers (Dashboard, booking actions, Gemini AI chatbot)
│   ├── signals.py               # Auto-reset slot states on cancellations/completions
│   ├── forms.py                 # Form representations for user inputs
│   └── urls.py                  # Booking and parking URL patterns
│
├── static/                      # Static Assets
│   └── css/
│       └── style.css            # Centralized styles (Glassmorphism layout, modal overlays)
│
├── templates/                   # HTML Template Layouts
│   ├── base.html                # Master layout (redesigned premium footer, Lucide script)
│   ├── accounts/
│   │   ├── login.html           # Authentication login template
│   │   └── register.html        # Authentication sign-up template
│   └── parking/
│       ├── dashboard.html       # User dashboard & Active Reservation tracker
│       ├── booking_history.html # Historic logs and reservation invoices
│       ├── book_slot.html       # Active slot booking interface
│       ├── explore_locations.html # Search and location discovery page
│       ├── verify_ticket.html   # QR code ticket details
│       └── payment.html         # Payment mock terminal
│
├── requirements.txt             # Python packages & dependencies
├── vercel.json                  # Serverless deployment configuration
├── db.sqlite3                   # Local SQLite database (git-ignored)
└── manage.py                    # Django CLI management script
```

---

## 🛠️ Database Schema

### 1. `User` (Custom Model)
*   Inherits from Django's `AbstractUser`
*   `phone`: `CharField` (max length 15) to store user contact details.

### 2. `Location`
*   `city`: `CharField`
*   `area`: `CharField`
*   `name`: `CharField`
*   `location_type`: `CharField` (Choices: Mall, Hotel, College, Office, Restaurant)

### 3. `ParkingSlot`
*   `location`: ForeignKey to `Location`
*   `slot_number`: `CharField`
*   `is_available`: `BooleanField` (Tracks live slot state)

### 4. `Booking`
*   `user`: ForeignKey to Custom `User`
*   `slot`: ForeignKey to `ParkingSlot`
*   `vehicle_number`: `CharField`
*   `booking_date`: `DateField`
*   `start_time`: `TimeField`
*   `end_time`: `TimeField`
*   `total_hours`: `FloatField`
*   `total_amount`: `FloatField`
*   `status`: `CharField` (Choices: PENDING, ACTIVE, CANCELLED)
*   `created_at`: `DateTimeField`

---

## 🚀 Installation & Local Setup

Follow these steps to run the project locally:

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on your system.

### 2. Clone and Navigate
Clone this repository to your local machine and enter the project folder:
```bash
git clone https://github.com/Sumit12312299/Parking-Management-System.git
cd Parking-Management-System
```

### 3. Install Dependencies
Install all required modules from the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
Prepare the SQLite database schema:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Admin Access)
Create an admin user to manage locations and slot lists:
```bash
python manage.py createsuperuser
```

### 6. Run the Server
Launch the local development web server:
```bash
python manage.py runserver
```
Visit the application in your browser at: **`http://127.0.0.1:8000`**

---

## 🌐 Deployment on Vercel

The application is fully configured for deployment on Vercel. 
*   It includes a `vercel.json` file configuring the WSGI handler for serverless environments.
*   It handles SQLite database setup in `/tmp/db.sqlite3` dynamically to prevent read-only errors on serverless lambdas.
*   Static files are compressed and cached automatically using **WhiteNoise**.

---

## 📜 License
This project is licensed under the MIT License - see the `LICENSE` file for details.