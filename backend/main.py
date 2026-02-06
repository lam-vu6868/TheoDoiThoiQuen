from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def Home():
    """
    Health check endpoint (ASYNC VERSION)
    Kiểm tra server có đang chạy không
    """
    return {"message":"Server đang chạy ngon lành"}



