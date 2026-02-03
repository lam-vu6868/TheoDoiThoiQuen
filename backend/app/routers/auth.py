from fastapi import HTTPException, Depends,APIRouter,status

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)
