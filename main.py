from fastapi import FastAPI
from authtuna import init_app

app = FastAPI()

init_app(app)


@app.get("/", tags=["Root"])
async def root():
    """
    A public endpoint that anyone can access.
    """
    return {"message": "Authentication Powered by AuthTuna!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000, host="0.0.0.0")
