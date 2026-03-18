# 🎯 Habit Tracker API

API Backend cho ứng dụng theo dõi thói quen (Habit Tracker) được xây dựng bằng **FastAPI** và **PostgreSQL**.

---

## 📋 Yêu cầu hệ thống

- Python 3.10+
- PostgreSQL 12+
- pip (Python package manager)

---

## 🚀 Cài đặt

### 1. Clone repository

```bash
git clone <repository-url>
cd backend
```

### 2. Tạo môi trường ảo (Virtual Environment)

````bash
# Windows
python -m venv venv
venv\Scripts\activate



### 3. Cài đặt thư viện

```bash
pip install -r requirements.txt
````

---

## ⚙️ Cấu hình

### 1. Tạo file `.env` trong thư mục `backend/`

### 2. Chỉnh sửa file `.env` với thông tin của bạn:

```env
# ========== Database ===========
DATABASE_URL=postgresql://username:password@localhost:5432/habit_tracker

# =========== SECURITY & JWT =========
# Tạo SECRET_KEY bằng lệnh: python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
# Token hết hạn sau 1 ngày (1440 phút)
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# ============= FRONTEND (cho CORS) ============
FRONTEND_URL=http://localhost:5500
```

### 3. Tạo database trong PostgreSQL

```sql
CREATE DATABASE habit_tracker;
```

### 4. Chạy migration (tạo bảng)

```bash
# Khởi tạo Alembic (chỉ lần đầu)
alembic init alembic

# Tạo migration tự động
alembic revision --autogenerate -m "Initial migration"

# Chạy migration
alembic upgrade head
```

---

## 🏃 Chạy server

### Development (có auto-reload)

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Server sẽ chạy tại: **http://localhost:8000**

---

## 📚 API Documentation

Sau khi chạy server, truy cập:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📁 Cấu trúc thư mục

```
backend/
├── app/
│   ├── core/              # Cấu hình core
│   │   ├── config.py      # Đọc biến môi trường từ .env
│   │   ├── database.py    # Kết nối SQLAlchemy
│   │   └── security.py    # JWT token & hash password
│   │
│   ├── models/            # SQLAlchemy models (bảng database)
│   │   ├── user.py
│   │   ├── habit.py
│   │   └── habit_log.py
│   │
│   ├── schemas/           # Pydantic schemas (validation)
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── habit.py
│   │   ├── habit_log.py
│   │   └── motivation.py
│   │
│   ├── routers/           # API endpoints
│   │   ├── auth.py        # Login, Register
│   │   ├── user.py        # User management
│   │   └── habit.py       # Habit CRUD
│   │
│   └── dependencies.py    # Dependency injection (get_current_user)
│
├── main.py                # Entry point
├── requirements.txt       # Thư viện Python
├── .env                   # Biến môi trường (KHÔNG COMMIT)
├── .env.example           # Mẫu file .env
├── .gitignore
└── README.md
```

---

## 🔑 API Endpoints chính

### Authentication

- `POST /auth/register` - Đăng ký tài khoản
- `POST /auth/login` - Đăng nhập (nhận token)

### User

- `GET /users/me` - Lấy thông tin profile
- `PUT /users/me` - Cập nhật profile
- `POST /users/change-password` - Đổi mật khẩu

### Habits

- `GET /habits` - Danh sách thói quen của user
- `POST /habits` - Tạo thói quen mới
- `PUT /habits/{id}` - Cập nhật thói quen
- `DELETE /habits/{id}` - Xóa thói quen

### Habit Logs

- `GET /logs` - Lịch sử check-in
- `POST /logs` - Check-in thói quen hôm nay
- `GET /logs/stats` - Thống kê (streak, total)

---

## 🔐 Authentication

API sử dụng **JWT Bearer Token**. Sau khi login, thêm token vào header:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Ví dụ với cURL:

```bash
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Ví dụ với JavaScript:

```javascript
fetch("http://localhost:8000/users/me", {
  headers: {
    Authorization: "Bearer " + token,
  },
});
```

---

## 🧪 Testing

```bash
# Chạy tests
pytest

# Với coverage
pytest --cov=app
```

---

## 🐛 Troubleshooting

### Lỗi: "pydantic_settings could not be resolved"

```bash
pip install pydantic-settings
```

### Lỗi: "connection to server failed"

- Kiểm tra PostgreSQL đã chạy chưa
- Kiểm tra DATABASE_URL trong .env đúng chưa

### Lỗi: "module 'app.models.user' has no attribute 'User'"

- Chưa tạo models → Code models trước
- Chưa chạy migration → Chạy `alembic upgrade head`

---

## 📝 Notes

- File `.env` chứa thông tin nhạy cảm → **KHÔNG ĐƯỢC COMMIT lên Git**
- SECRET_KEY phải mạnh và unique cho mỗi môi trường
- Token mặc định hết hạn sau 1 ngày (1440 phút)
- Database cần PostgreSQL (không dùng SQLite cho production)

---

## 👥 Team / Contributors

- **Developer**: [Tên bạn]
- **Contact**: [Email]

---

## 📄 License

MIT License
