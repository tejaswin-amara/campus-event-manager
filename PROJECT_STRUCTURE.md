# Project Structure Overview

This document provides a detailed breakdown of the **Campus Event Manager** codebase, organized by responsibility and layer.

## 📂 Project Root
- `pom.xml`: Maven configuration, dependencies (Spring Boot, JPA, MySQL, etc.), and build settings.
- `README.md` & `TECHNICAL_GUIDE.md`: Project documentation and setup instructions.
- `run_app.ps1` / `stop_app.ps1`: Convenience scripts for starting and stopping the application locally.
- `uploads/`: Local directory where event images are stored after being uploaded via the Admin Dashboard.

---

## 📦 Backend (`src/main/java/com/tejaswin/campus`)
The Java source code is organized into a clean 3-tier architecture:

### 🧩 Models (`/model`)
Entities representing the database schema.
- `User.java`: Defines Admin and Student users with role-based access.
- `Event.java`: Main entity for campus events (title, date, venue, category, etc.).
- `Registration.java`: Links users to events to track interest and analytics.

### 💾 Repositories (`/repository`)
JPA Interfaces for database communication and complex query derivation.
- `UserRepository`, `EventRepository`, `RegistrationRepository`.

### ⚙️ Services (`/service`)
Business logic layer.
- `EventService.java`: Handles CSV exports, image cleanup logic, N+1 query optimization, and event registration.
- `UserService.java`: Handles user authentication and role management.

### 🎮 Controllers (`/controller`)
HTTP request handlers.
- `AuthController.java`: Manages Login/Logout for both Students and Admins.
- `EventController.java`: Manages the Student Dashboard and event engagement.
- `AdminController.java`: Manages the Admin Dashboard (CRUD, Analytics, Exports).

### 🛠️ Configuration & Core
- `config/WebMvcConfig.java`: Configures static resource paths for external file access (images).
- `exception/GlobalExceptionHandler.java`: Centralized error handling for file size limits and 404s.
- `CampusEventManagerApplication.java`: The Spring Boot entry point.

---

## 🎨 Frontend & Resources (`src/main/resources`)

### 🏙️ Templates (`/templates`)
Thymeleaf HTML templates (Dynamic Content).
- `dashboard.html`: Main UI for students to view/interact with events.
- `admin_dashboard.html`: Management console with real-time analytics.
- `admin_login.html`: Secure administrative entry point.
- `error.html`: Polished, animated fallback page for application errors.

### 🛠️ Static Assets (`/static`)
- `css/style.css`: Core design system (Glassmorphism, Dark Theme, Animations).
- `js/`: Frontend logic for search, category filtering, and Chart.js integration.
- `sw.js` & `manifest.json`: Progressive Web App (PWA) configuration for offline use and mobile installation.

### 📝 Properties
- `application.properties`: Main config for database, server ports, and file upload constraints.

---

## 🧪 Tests (`src/test/java`)
- `EventServiceTest.java`: JUnit/Mockito suites verifying critical business logic without requiring a live database.
