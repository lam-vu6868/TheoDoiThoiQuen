# 📝 DANH SÁCH FILE CẦN CODE - HABIT TRACKER

## ✅ ĐÃ CÓ SẴN:

- ✅ `app/models/model.py` - Tất cả models
- ✅ `app/core/config.py` - Config
- ✅ `app/core/database.py` - Database connection
- ✅ `app/core/security.py` - JWT & password hashing
- ✅ `app/crud/*.py` - Tất cả CRUD operations (5 files)
- ✅ `app/utils/*.py` - Validators, formatters, constants
- ✅ `app/schemas/user.py` - User schemas
- ✅ `app/routers/auth.py` - Auth router (login/register)
- ✅ `app/routers/user.py` - User router
- ✅ `alembic/env.py` - Alembic config

---

## 🚀 DANH SÁCH FILE CẦN TẠO (THEO THỨ TỰ)

### 🔴 **1. Chạy Migration (BẮT BUỘC TRƯỚC KHI CODE)**

```bash
cd d:\TheoDoiThoiQuen\backend
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

**→ Tạo 6 bảng trong database**

---

### 🔴 **2. backend/.gitignore** (BẮT BUỘC)

**Tránh commit .env, venv lên Git**

---

### 🔴 **3. backend/.env.example**

**Template cho .env**

---

### 🟠 **4. app/schemas/auth.py**

**Chứa:** Token, LoginRequest, RegisterRequest

---

### 🟠 **5. app/schemas/habit.py**

**Chứa:** HabitBase, HabitCreate, HabitUpdate, Habit, HabitWithStats

---

### 🟠 **6. app/schemas/habit_log.py**

**Chứa:** HabitLogBase, HabitLogCreate, HabitLogUpdate, HabitLog

---

### 🟠 **7. app/schemas/quote.py**

**Chứa:** QuoteBase, QuoteCreate, Quote

---

### 🟢 **8. app/schemas/session.py** (Optional)

**Chứa:** SessionBase, Session

---

### 🟠 **9. app/routers/habit.py**

**Endpoints:** GET/POST/PUT/DELETE `/habits`

---

### 🟠 **10. app/routers/habit_log.py**

**Endpoints:** GET/POST/PUT/DELETE `/logs`, GET `/logs/stats`

---

### 🟠 **11. app/routers/quote.py**

**Endpoints:** GET `/quotes/random`, POST/DELETE `/quotes` (admin)

---

## ✅ THỨ TỰ KHUYẾN NGHỊ:

1. **Chạy migration** → Tạo tables
2. **Tạo .gitignore** → Bảo mật
3. **Code schemas/auth.py** → Để test login/register
4. **Test Auth** → Đảm bảo login/register hoạt động
5. **Code schemas/habit.py + routers/habit.py** → CRUD habits
6. **Test Habits** → Tạo/sửa/xóa habits
7. **Code schemas/habit_log.py + routers/habit_log.py** → Check-in
8. **Test Habit Logs** → Check-in và xem stats
9. **Code schemas/quote.py + routers/quote.py** → Quote random
10. **Test toàn bộ flow** → Đăng ký → Login → Tạo habit → Check-in

---

## 🎯 NHANH NHẤT (MVP):

**Bỏ qua:** schemas/session.py, routers/quote.py (làm sau)

**Tập trung:**

1. Migration
2. .gitignore
3. Auth schemas (đã có router)
4. Habit schemas + router
5. Habit Log schemas + router
6. **→ TEST XEM ĐÃ HOẠT ĐỘNG CHƯA!**

---

## 🚀 LỆNH TEST:

```bash
cd d:\TheoDoiThoiQuen\backend
uvicorn main:app --reload
```

**Mở:** `http://localhost:8000/docs`
