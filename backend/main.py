from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError  # Import exception type
from app.routers import auth  # Import router auth
from app.core.exceptions import validation_exception_handler  # Import custom handler

app = FastAPI(
    title="API Theo Dõi Thói Quen",
    description="API quản lý thói quen người dùng",
    version="1.0.0"
)

# ===== ĐĂNG KÝ CUSTOM EXCEPTION HANDLER =====
# Mọi lỗi validation (422) sẽ đi qua validation_exception_handler
# để chuyển đổi message tiếng Anh → tiếng Việt
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Đăng ký các routers
app.include_router(auth.router)  # Đăng ký router auth (/auth/register, /auth/login...)


@app.get("/", tags=["Health Check"])
async def Home():
    return {"message":"Server đang chạy ngon lành"}



