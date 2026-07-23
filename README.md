# 🚗 ParkKaro - Premium Parking Management System

<img width="1920" height="1080" alt="ParkKaro Banner" src="https://github.com/user-attachments/assets/effa32eb-6ab5-4686-a5cd-cd00e17d9869" />

**ParkKaro** is a modern, premium web-based Parking Management System built on Django. It enables users to browse nearby parking structures, view slot availability in real-time, interact with slots dynamically, and book them securely with seamless animations and an AI-powered helper chatbot.

---

## ✨ Features

- 🗺️ **Interactive Location Explorer:** Filter parking zones by city and area to find parking spaces near malls, restaurants, and offices.
- 🚦 **Real-Time Slot Visualization:** Dynamic grid rendering where occupied, reserved, and available slots are clearly visualized.
- 🔑 **On-Demand Authentication:** Guests can browse locations and slots freely. The application prompts login/registration only at the moment of booking and returns users directly to their selected slot.
- 💳 **GPay-Style Mock Payment System:** Seamless transaction flow complete with an authentic verification spinner and checked status feedback.
- 🤖 **ParkBot - AI Assistant:** Floating support widget powered by the Google Gemini API to assist users with reservations, venue policies, and general support.
- 📈 **Dynamic Booking Dashboard:** Visual records of historical logs, active bookings, ticket verification, and cancellation options.

---

## 🎨 Design & Premium Animations

The frontend is built using **Vanilla CSS** and customized interactions to create a state-of-the-art UI:
- **Viewport-Triggered Counters:** Numbers roll up organically using an `IntersectionObserver` when scrolled into view.
- **Staggered Card Entrances:** Location and feature cards slide up with custom timing delays for a fluid entrance.
- **Glassmorphism Navbar:** Transparent, sticky header with backdrop blur and active link underlines.
- **Shimmering Buttons:** Interactive call-to-actions feature a reflective sweep gradient to capture user attention.
- **Floating Hero Cards:** Stats container loops in a gentle floating motion to add depth.
- **Micro-interactions:** Icons rotate, scale, and cards glow on cursor hover.

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML5, CSS3, JavaScript (ES6)
- **Icons:** Lucide Icons
- **AI Model Integration:** Google Gemini API
- **Database:** SQLite (development) / PostgreSQL (production)

---

## 🚀 Installation & Setup

Follow these steps to set up the project locally:

### 1. Clone the Repository
```bash
git clone https://github.com/Sumit12312299/Parking-Management-System.git
cd Parking-Management-System
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Start Development Server
```bash
python manage.py runserver
```
Visit the local server at `http://127.0.0.1:8000/` in your browser.

### 6. Run Automated Unit Tests
```bash
python manage.py test
```
Runs the full suite of unit tests for model validation, slot availability logic, and user authentication views.

---

## 📂 Project Structure

```
├── accounts/               # User authentication, registration, login views & custom admin
├── parking/                # Booking engine, slot management, unit tests & AI Chatbot
├── templates/              # HTML layout templates (including custom 404 & 500 error pages)
├── static/                 # CSS styling sheets, images, and JS
├── config/                 # Base Django project configuration settings
├── .env.example            # Environment variables configuration template
└── manage.py               # Django utility script
```

---

## 📝 License
Distributed under the MIT License. See `LICENSE` for more information.

