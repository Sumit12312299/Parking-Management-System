# Software Requirements Specification (SRS) & System Design
**Project:** ParkKaro (Parking Management System)
**Version:** 1.0

---

## 1. Problem Identification & Objective

### 1.1 The Problem
In rapidly growing urban environments, finding an available parking spot in commercial areas (malls, hospitals, offices) is a major challenge. 
* **Time & Fuel Wastage:** Drivers spend excessive time circling for parking, leading to fuel waste and increased traffic congestion.
* **Lack of Real-time Visibility:** Drivers have no way of knowing if a parking lot is full before arriving.
* **Inefficient Management:** Manual ticketing systems are prone to human error, cash handling issues, and lack data analytics for parking operators.

### 1.2 The Solution (ParkKaro)
ParkKaro is a centralized web-based parking management system that allows users to:
* Discover nearby parking locations and view real-time slot availability.
* Pre-book premium parking slots via an interactive graphical seat-map.
* Manage their bookings (Extend time, Cancel bookings) dynamically.
* Utilize digital E-Tickets (QR Codes) for seamless entry and exit.

---

## 2. High-Level Design (HLD)

The High-Level Design outlines the overall architecture of the application. ParkKaro follows a classic **Model-Template-View (MTV)** architecture powered by the Django web framework.

### 2.1 System Architecture

```mermaid
graph TD
    Client[Client Browser / Mobile] -->|HTTP/HTTPS| WebServer[Web Server / Gunicorn]
    WebServer -->|WSGI| DjangoApp[Django Application]
    
    subgraph Django Backend
        Views[Views / Controllers]
        Models[Models / ORM]
        Templates[HTML / Django Templates]
    end
    
    DjangoApp --> Views
    Views <--> Models
    Views <--> Templates
    Templates -->|Renders UI| Client
    
    Models <-->|SQL Queries| Database[(Relational Database)]
    Views -->|Fetch QR| ExternalAPI[QR Code API]
```

### 2.2 Core Modules
1. **Authentication Module:** Handles user registration, login, and session management.
2. **Location & Slot Module:** Manages parking locations and individual slot states (Available/Booked).
3. **Booking & Transaction Module:** Handles reservation logic, time calculations, pricing, cancellations, and time extensions.

---

## 3. Low-Level Design (LLD)

The Low-Level Design defines the database schema and the specific interactions between internal components.

### 3.1 Entity-Relationship Diagram (ERD)

```mermaid
erDiagram
    USER ||--o{ BOOKING : makes
    LOCATION ||--o{ PARKING_SLOT : contains
    PARKING_SLOT ||--o{ BOOKING : "has (temporal)"

    USER {
        int id PK
        string username
        string email
        string password
    }

    LOCATION {
        int id PK
        string name
        string city
        string area
        int total_slots
    }

    PARKING_SLOT {
        int id PK
        int location_id FK
        string slot_number
        boolean is_available
    }

    BOOKING {
        int id PK
        int user_id FK
        int slot_id FK
        string vehicle_number
        date booking_date
        time start_time
        time end_time
        float total_amount
        string status "ACTIVE/CANCELLED"
    }
```

### 3.2 Key Algorithms & Logic
* **Slot Availability Check:** A slot is marked `is_available = False` immediately upon a successful booking. In a production environment, cron jobs or background tasks (Celery) would monitor the `end_time` and automatically revert the slot to `True` when the booking expires.
* **Refund Calculation Logic:** If a user cancels an active booking, a 10% cancellation fee is deducted from the `total_amount` (with a minimum cap of ₹5 and a maximum cap of the total amount).
* **Extension Logic:** Extending a booking adds hours to the `end_time` and strictly calculates additional charges (e.g., +₹20 per hour) dynamically without requiring a new booking entry.

---

## 4. User Flow & Sequence Diagrams

### 4.1 Booking Sequence Flow
The following diagram illustrates the exact chronological flow when a user attempts to book a parking slot.

```mermaid
sequenceDiagram
    actor User
    participant Frontend as UI (Dashboard)
    participant Views as Django Views
    participant DB as Database
    participant QR as External QR API

    User->>Frontend: Selects Location & Clicks "View Slots"
    Frontend->>Views: GET /location/{id}/
    Views->>DB: Query Available Slots
    DB-->>Views: Return Slots list
    Views-->>Frontend: Render Interactive Parking Map

    User->>Frontend: Clicks an Available Slot
    Frontend->>Views: GET /book/{slot_id}/
    Views-->>Frontend: Render Booking Form

    User->>Frontend: Submits Date, Time & Vehicle Number
    Frontend->>Views: POST /book/{slot_id}/
    Views->>DB: Calculate Amount & Create Pending Booking
    DB-->>Views: Booking ID generated
    Views-->>Frontend: Redirect to Payment Page

    User->>Frontend: Clicks "Pay Securely"
    Frontend->>Views: POST /payment/{booking_id}/
    Views->>DB: Update Booking Status to ACTIVE
    Views->>DB: Set Slot is_available = False
    DB-->>Views: Success
    Views-->>Frontend: Redirect to Booking History

    User->>Frontend: Clicks "Ticket"
    Frontend->>QR: Request QR Code with Booking ID
    QR-->>Frontend: Return QR Image
    Frontend-->>User: Display E-Ticket Popup
```

---

## 5. Non-Functional Requirements
1. **Responsiveness:** The UI (Interactive map, History cards) must adapt to mobile devices.
2. **Usability:** Implement a strict visual hierarchy using premium CSS (Glassmorphism, hover interactions) to reduce user cognitive load.
3. **Security:** Implement CSRF protection on all forms and ensure user data (passwords) is hashed using Django's default PBKDF2 algorithm.

---
*Document Generated for ParkKaro - 2026*
