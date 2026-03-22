from fastapi import FastAPI

app = FastAPI()


@app.get("/")  # get, post, put, delete, patch
async def root():
    return {"message": "Hello from Algo-Notes"}
