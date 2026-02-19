# 🎓 Campus Event Manager

<div align="center">

![Java](https://img.shields.io/badge/Java-21-orange)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.2-green)
![Thymeleaf](https://img.shields.io/badge/Thymeleaf-Frontend-blue)
![MySQL](https://img.shields.io/badge/MySQL-Database-lightblue)
![PWA](https://img.shields.io/badge/PWA-Ready-purple)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

**A modern, full-stack event management system for university campuses.**
Allows students to register for events and admins to manage them with ease.

[Student Dashboard](http://localhost:9090/) • [Admin Panel](http://localhost:9090/admin/login)

</div>

---

## ✨ Features 2.0 (Ultimate Edition)

| 🧑‍🎓 Student Dashboard | 👨‍💼 Admin Management Panel |
| :--- | :--- |
| **Fast Category Switching**: Interactive sidebar with skeleton loaders. | **Full Event Control**: Create, update, and manage with ease. |
| **Dynamic QR Codes**: Instant registration QR codes for every event. | **CSV Export**: Full database export for offline analysis. |
| **Add to Calendar**: One-click ICS generation for Google/Outlook. | **Interactive Analytics**: Dynamic Chart.js visualizations. |
| **Premium Toasts**: Animated notifications for fluid feedback. | **Zero-Overflow Layout**: Optimized for high-density data. |
| **Mobile-First Design**: Glassmorphism and micro-animations. | **SEO Optimized**: Open Graph tags for rich social sharing. |
| **Time Filters**: Filter events by Upcoming, Ongoing, & Past. | **Auto-Cleanup**: Automatically deletes images when removing events. |

---

## 🚀 Quick Start (PowerShell)

### 1️⃣ Run the Application
**Run this in your terminal:**
```powershell
.\run_app.ps1
```

> **Automated Workflow:**
> ✅ Starts **MySQL Service**
> ✅ Builds the **Java Spring Boot App**
> ✅ Opens the app in your browser at **http://localhost:9090**

### 2️⃣ Stop & Restart 
*   **Stop**: Press `Ctrl + C` in the terminal.
*   **Forced Stop**: `.\stop_app.ps1` (Kills port 9090 conflicts).
*   **Restart**: Just run `.\run_app.ps1` again.

---

## 🔑 Access Details

| Application Link | Credentials |
| :--- | :--- |
| **Student** | [Localhost:9090](http://localhost:9090/) (Guest Login) |
| **Admin** | [Localhost:9090/admin/login](http://localhost:9090/admin/login) (`admin` / `admin123`) |

---

## 🐳 Docker

```bash
# Build and run
docker build -t campus-events .
docker run -p 9090:9090 \
  -e DB_URL=jdbc:mysql://host.docker.internal:3306/campus_events?createDatabaseIfNotExist=true \
  -e DB_USERNAME=root \
  -e DB_PASSWORD=root \
  campus-events
```

---

## ⚙️ Environment Variables

| Variable | Default | Description |
| :--- | :--- | :--- |
| `PORT` | `9090` | Server port |
| `DB_URL` | `jdbc:mysql://localhost:3306/campus_events?...` | JDBC connection URL |
| `DB_USERNAME` | `root` | Database username |
| `DB_PASSWORD` | `root` | Database password |
| `DDL_AUTO` | `update` | Hibernate DDL mode (`update`, `validate`, `none`) |
| `ADMIN_PASSWORD` | `admin123` | Initial admin password |
| `UPLOAD_DIR` | `uploads` | Directory for uploaded images |
| `LOG_LEVEL` | `DEBUG` | Logging level |

---

## 🔗 API Endpoints

| Method | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Root → auto-login as guest → redirect to student dashboard |
| `GET` | `/admin/login` | Admin login page |
| `POST` | `/admin/login` | Admin authentication |
| `GET` | `/admin/dashboard` | Admin dashboard & analytics |
| `POST` | `/admin/events/add` | Create new event |
| `POST` | `/admin/events/edit/{id}` | Update event |
| `POST` | `/admin/events/delete/{id}` | Delete event |
| `GET` | `/admin/events/export/csv` | Export events as CSV |
| `GET` | `/student/dashboard` | Student event listing |
| `GET` | `/student/event/{id}` | Event detail (redirect to dashboard) |
| `GET` | `/student/register-external/{id}` | Redirect to external registration |

---

## 📂 Structure Overview

```bash
📦 Campus Event Manager
 ┣ 📜 run_app.ps1     # Integrated startup script (App + DB)
 ┣ 📜 stop_app.ps1    # Emergency port killer
 ┣ 📜 Dockerfile      # Multi-stage Docker build
 ┣ 📜 .dockerignore   # Docker context exclusions
 ┗ 📂 src/main/resources
   ┣ 📂 static        # CSS, Micro-animations, PWA Assets
   ┗ 📂 templates     # Thymeleaf HTML Views
```

<div align="center">
  <sub>Modernized for Advanced Agentic Coding</sub>
</div>
