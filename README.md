# CampusRetain 🎒🔍

**CampusRetain** is a modern, premium "Lost and Found" web application tailored specifically for university campuses. Built for speed, security, and usability, the platform connects students who have lost their belongings with those who have found them, complete with a secure verification system to prevent fraudulent claims.

---

## 👥 Team Codex
Developed with ❤️ by **Team Codex** for the Hackathon.

### Meet the Team
- **Vishvanth** – Team Lead
- **Madhusudhan Ramshetty** – Member
- **Varsha HC** – Member

---

## ✨ Key Features
- **Student Authentication Portals:** Users securely log in using strict organization email domain verification (e.g., `@ced.alliance.edu.in`), preventing outsiders from spamming the system.
- **Modern UI/UX:** Built using Tailwind CSS, featuring glassmorphism design, interactive loading states, smooth modal transitions, and non-intrusive toast notification alerts.
- **Reporting System (Base64 Native):** Finders can log lost items with categories, locations, and photo uploads. Images are securely converted into Base64 strings and stored directly in the database to prevent ephemeral storage wipes.
- **Verification Logic:** Finders can list a "Secret Detail" that is hidden from the public feed. When claiming, users must provide verification proof matching this secret detail to prove ownership.
- **Admin Dashboard:** A dedicated, secure dashboard for administrators to view overarching statistics, review queued claims, and securely approve or delete items from the database.
- **Automated Notifications:** 
  - **Twilio SMS:** Direct SMS notification system instantly pings claim statuses directly to the user's mobile device via Twilio.

---

## 🛠️ Tech Stack
- **Backend:** Python 3, Flask
- **Database:** PostgreSQL capable (via SQLAlchemy ORM) / Fallback to SQLite
- **Frontend:** HTML5, Vanilla JavaScript, Tailwind CSS (CDN)
- **Deployment & Cloud:** Fully configured for **Zoho Catalyst AppSail** serverless deployment.

---

## 🚀 Running Locally

### 1. Requirements
Ensure you have Python 3 and `pip` installed on your machine.

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

Open your browser and navigate to `http://127.0.0.1:9000`.

### 4. Demo Credentials
To access the Admin view, navigate to `/admin_login` and use the following MVP testing credentials:
- **Email:** `vishvanthbtech24@ced.alliance.edu.in`
- **Password:** `Life@789`

---

## ☁️ Deployment Guide (Zoho Catalyst)
This application is designed specifically to scale seamlessly on **Zoho Catalyst AppSail**. 

### 1. Environment Variables Configuration
Because serverless environments run on ephemeral containers, the local SQLite database resets on inactivity sleep. To maintain data persistency, add the underlying integrations to your **Zoho Catalyst AppSail -> Configuration -> Environment Variables**:
- `DATABASE_URL`: `postgresql://user:password@host/dbname`
- `TWILIO_ACCOUNT_SID`: `[Your Twilio SID]`
- `TWILIO_AUTH_TOKEN`: `[Your Twilio Token]`
- `TWILIO_PHONE_NUMBER`: `[Your Twilio Number]`

### 2. Deploying to the Cloud
Run the included deployment script located in your root directory:
```bash
chmod +x deploy.sh
./deploy.sh
```
This script automatically compiles your backend packages, static layouts, and syncs them directly securely to your cloud Zoho AppSail component.
