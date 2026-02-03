from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def Home():
    return {"message":"Server đang chạy ngon lành"}



