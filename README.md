# 🏔️ TrekSphere - Trek Management System

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.x-black)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue)
![License](https://img.shields.io/badge/License-MIT-green)

A role-based Trek Management Web Application developed using **Flask**, **SQLite**, **Bootstrap**, and **SQLAlchemy** that streamlines trek planning, staff management, and online booking through a centralized portal.

---

# Table of Contents

- Project Overview
- Problem Statement
- Objectives
- Key Features
- System Modules
- Admin Module
- Staff Module
- Trekker Module
- Booking Workflow
- Technology Stack
- Database Design
- Project Structure
- Installation Guide
- Screenshots
- Future Enhancements
- Contributors
- License

---

# Project Overview

TrekSphere is a web-based Trek Management System designed for trekking clubs, adventure organizations, and tourism companies.

Instead of managing treks manually through spreadsheets, WhatsApp groups, phone calls, or paper records, TrekSphere centralizes every operation into one secure web application.

The application provides three dedicated dashboards:

- Admin Dashboard
- Staff Dashboard
- Trekker Dashboard

Each user can access only the features allowed according to their role.

---

# Problem Statement

Adventure organizations usually face several operational challenges:

- Manual registration process
- Duplicate bookings
- Overbooking
- Difficulty assigning trek leaders
- Lack of booking history
- Poor communication
- No centralized database
- Time-consuming management

TrekSphere eliminates these issues through an automated role-based system.

---

# Objectives

The project aims to:

- Digitize trekking management.
- Provide secure role-based access.
- Simplify trek booking.
- Prevent duplicate bookings.
- Prevent overbooking.
- Maintain trek history.
- Approve staff before granting access.
- Provide an organized dashboard for every user.

---

# Key Features

## Authentication

- Secure Login
- Registration
- Password Hashing
- Session Management
- Logout
- Role Based Authentication

---

## Trek Management

Admin can

- Create Trek
- Edit Trek
- Delete Trek
- Assign Staff
- Open/Close Trek
- Update Trek Details

Each trek stores

- Name
- Location
- Difficulty
- Duration
- Available Slots
- Description
- Start Date
- End Date
- Assigned Staff
- Status

---

## Booking System

Trekkers can

- View Open Treks
- Filter Treks
- Book Trek
- Cancel Booking
- View Booking History

The application automatically

- Prevents duplicate bookings
- Prevents overbooking
- Tracks booking status

---

## Staff Approval

Staff registration requires Admin approval.

Workflow

Staff Register

↓

Pending Approval

↓

Admin Approves

↓

Dashboard Access

---

## Search System

Admin can search

- Trek ID
- Trek Name
- User ID
- User Name
- Staff Name
- Email

---

# User Roles

## 👑 Admin

Admin controls the complete application.

### Functionalities

- Dashboard
- Create Trek
- Edit Trek
- Delete Trek
- Assign Staff
- Approve Staff
- Blacklist Users
- Blacklist Staff
- Search Records
- View Statistics

---

## 🧗 Trek Staff

Staff members are responsible for operational activities.

### Functionalities

- View Assigned Treks
- Update Trek Status
- Update Available Slots
- View Participants
- Manage Trek Information

---

## 🎒 Trekker

Trekkers are end users of the system.

### Functionalities

- Register
- Login
- Browse Treks
- Search Treks
- Filter Treks
- Book Trek
- Cancel Booking
- Booking History

---

# Booking Workflow

```
Admin Creates Trek
        │
        ▼
Assign Staff
        │
        ▼
Open Trek
        │
        ▼
Trekkers View Trek
        │
        ▼
Book Trek
        │
        ▼
Booking Stored
        │
        ▼
Dashboard Updated
```

---

# Technology Stack

## Backend

- Python
- Flask
- Flask SQLAlchemy
- Werkzeug

## Frontend

- HTML5
- CSS3
- Bootstrap 5
- Jinja2

## Database

- SQLite

## Version Control

- Git
- GitHub

---

# Database Design

## User Table

Contains

- ID
- Name
- Email
- Phone
- Password Hash
- Role
- Approved
- Blacklisted

---

## Trek Table

Contains

- Trek ID
- Trek Name
- Location
- Difficulty
- Duration
- Slots
- Description
- Start Date
- End Date
- Staff ID
- Status

---

## Booking Table

Contains

- Booking ID
- User ID
- Trek ID
- Booking Date
- Booking Status

---

# Project Structure

```
TrekSphere/
│
├── app.py
├── config.py
├── extensions.py
├── models.py
├── requirements.txt
├── README.md
│
├── routes/
│   ├── admin.py
│   ├── auth.py
│   ├── main.py
│   ├── staff.py
│   └── user.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── pending_approval.html
│   │
│   ├── admin/
│   ├── staff/
│   └── user/
│
├── static/
│   ├── css/
│   ├── images/
│   └── js/
│
├── instance/
│   └── trekking.db
│
└── utils.py
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/TrekSphere.git
```

## Open Folder

```bash
cd TrekSphere
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

## Install Packages

```bash
pip install -r requirements.txt
```

## Run Project

```bash
python app.py
```

Open Browser

```
http://127.0.0.1:5000
```

---

# Screenshots

Add screenshots of

- Home Page
- Login Page
- Register Page
- Admin Dashboard
- Staff Dashboard
- Trekker Dashboard
- Trek Management
- Booking History

---

# Security Features

- Password Hashing
- Session Authentication
- Role Based Access
- Staff Approval
- User Blacklisting
- Duplicate Booking Prevention
- Overbooking Prevention

---

# Future Enhancements

- Payment Gateway
- Google Maps Integration
- Trek Images
- Email Notifications
- SMS Alerts
- QR Code Tickets
- Download Booking Receipt
- Online Chat Support
- Reviews & Ratings
- Weather API
- AI Trek Recommendation
- Live Trek Tracking
- Emergency SOS Feature

---
---

# Conclusion

TrekSphere demonstrates how role-based authentication, secure database management, and structured workflows can simplify trekking operations.

The application provides a complete ecosystem for administrators, staff members, and trekkers while maintaining security, efficiency, and ease of use.

This project serves as an excellent academic project and can be further extended into a production-ready adventure management platform.
