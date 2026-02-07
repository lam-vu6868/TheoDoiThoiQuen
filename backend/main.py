from fastapi import FastAPI
from app.routers import auth  # Import router auth

app = FastAPI(
    title="API Theo Dõi Thói Quen",
    description="API quản lý thói quen người dùng",
    version="1.0.0"
)

# Đăng ký các routers
app.include_router(auth.router)  # Đăng ký router auth (/auth/register, /auth/login...)


@app.get("/", tags=["Health Check"])
async def Home():
    """
    Health check endpoint (ASYNC VERSION)
    Kiểm tra server có đang chạy không
    """
    return {"message":"Server đang chạy ngon lành"}



