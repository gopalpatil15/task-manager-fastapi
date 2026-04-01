# 🚀 Task Manager API

A secure, production-ready RESTful API built using **FastAPI** and **PostgreSQL**, designed with clean architecture principles, authentication, and scalable backend practices.

---

## 🔥 Features

* **JWT Authentication** (OAuth2 Password Flow)
* **User-based Access Control** (multi-user support)
*  **Task Management System**
*  **Secure Password Hashing** using Bcrypt
*  **PostgreSQL Integration** with relational schema
*  **Input Validation** using Pydantic
*  **Interactive API Docs** via Swagger UI

---

## 🏗 Architecture Overview

This project follows a **modular backend structure**:

* **Routes Layer** → Handles API endpoints
* **Auth Layer** → JWT & security logic
* **Database Layer** → Connection + queries
* **Schema Layer** → Request/response validation

Designed for clarity, scalability, and maintainability.

---

## 🛠 Tech Stack

| Layer      | Technology        |
| ---------- | ----------------- |
| Backend    | FastAPI (Python)  |
| Database   | PostgreSQL        |
| Auth       | JWT (python-jose) |
| Security   | Passlib (Bcrypt)  |
| Validation | Pydantic          |
| Server     | Uvicorn           |

---

## 🔐 Authentication Flow

1. User registers → credentials stored securely
2. User logs in → receives JWT token
3. Token is used in protected routes

```http
Authorization: Bearer <your_token>
```

---

## 📡 API Endpoints

### 🔑 Authentication

| Method | Endpoint    | Description   |
| ------ | ----------- | ------------- |
| POST   | `/register` | Create user   |
| POST   | `/login`    | Get JWT token |

---

### 📋 Tasks (Protected)

| Method | Endpoint           | Description    |
| ------ | ------------------ | -------------- |
| GET    | `/tasks`           | Get user tasks |
| POST   | `/tasks`           | Create task    |
| PUT    | `/tasks/{task_id}` | Update task    |
| DELETE | `/tasks/{task_id}` | Delete task    |

✔ All operations are **user-specific** (secure isolation)

---

## ⚙️ Setup & Installation

### 1. Clone repository

```bash
git clone <your-repo-url>
cd task_manager
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create `.env` file:

```env
DB_HOST=localhost
DB_NAME=task_manager
DB_USER=postgres
DB_PASSWORD=yourpassword
SECRET_KEY=your_secret_key
```

---

### 4. Run server

```bash
uvicorn app.main:app --reload
```

---

### 5. Open API docs

👉 http://127.0.0.1:8000/docs

---

## 🧪 Sample Request

### Create Task

```bash
curl -X POST "http://127.0.0.1:8000/tasks" \
-H "Authorization: Bearer <token>" \
-H "Content-Type: application/json" \
-d '{"title": "Learn FastAPI", "priority": "high"}'
```

---

## 📌 Key Design Decisions

* Used **PostgreSQL over JSON** for real-world data persistence
* Implemented **JWT auth** for secure user sessions
* Enforced **user-level data isolation** in all queries
* Kept architecture **simple but scalable** (no over-engineering)

---

## 🚀 Future Improvements

* Pagination & filtering
* Docker deployment
* Async database support (asyncpg)
* Role-based access control
* CI/CD pipeline

---

## 💼 Why this Project Matters

This project demonstrates:

* Backend API development skills
* Authentication & security implementation
* Database design & relationships
* Clean and maintainable code structure

---

## 📄 License

MIT License
