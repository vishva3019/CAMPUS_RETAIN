# CampusRetain 🎒🔍

**CampusRetain** is a modern, premium "Lost and Found" web application tailored specifically for university campuses. Built for speed, security, and usability, the platform connects students who have lost their belongings with those who have found them, complete with a secure verification system to prevent fraudulent claims.

---

## ✨ Key Features
- **Student Authentication Portals:** Users securely log in using strict organization email domain verification (e.g., `@alliance.edu.in`), preventing outsiders from spamming the system.
- **Modern UI/UX:** Built using Tailwind CSS, featuring glassmorphism design, interactive loading states, smooth modal transitions, and non-intrusive toast notification alerts.
- **Reporting System:** Finders can easily log lost items with categories, locations, and photo uploads complete with live thumbnail previews.
- **Verification Logic:** Finders can list a "Secret Detail" that is hidden from the public feed. When claiming, users must provide verification proof matching this secret detail to prove ownership.
- **Admin Dashboard:** A dedicated, secure dashboard for administrators to view overarching statistics, review queued claims, and securely approve or delete items from the database.
- **Email Notifications:** Automated email dispatch via SMTP alerts students the moment their claim is submitted or approved by an administrator for pickup.

---

## 🛠️ Tech Stack
- **Backend:** Python 3, Flask
- **Database:** SQLite & SQLAlchemy (ORM)
- **Frontend:** HTML5, Vanilla JavaScript, Tailwind CSS (CDN)
- **Deployment Ready:** Configured with `gunicorn`, dynamic port binding, and `requirements.txt` for fast PaaS cloud deployment (Render/Heroku/Vercel).

---

## 🚀 Running Locally

### 1. Requirements
Ensure you have Python 3 and `pip` installed on your machine.
- macOS/Linux: `python3`
- Windows: `python`

### 2. Installation
Clone the repository and install the required dependencies:
```bash
git clone https://github.com/YourUsername/CampusRetain.git
cd CampusRetain
pip install -r requirements.txt
```

### 3. Execution
Start the Flask development server:
```bash
python3 app.py
```
*(On Windows, run `python app.py`)*

Open your browser and navigate to `http://127.0.0.1:5001`.

### 4. Demo Credentials
To access the Admin view, navigate to `/admin_login` and use the following MVP testing credentials:
- **Email:** `admin@alliance.edu.in`
- **Password:** `admin123`

---

## ☁️ Deployment Guide
This application is fully pre-configured for platforms like **Render.com**. 
1. Create a "New Web Service" on Render and link your GitHub Repo.
2. Select **Python 3** as the environment.
3. **Build Command:** `pip install -r requirements.txt`
4. **Start Command:** `gunicorn app:app`

*Note: Free cloud hosting tiers utilize ephemeral disks, which means local SQLite databases (like `campus_retain.db`) and uploaded images will reset on server restarts. For persistent production, upgrade to a managed PostgreSQL database.*

---

*Developed for the Hackathon.*
