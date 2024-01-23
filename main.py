from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import auth

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.add_middleware(SessionMiddleware, secret_key='qrdssrf2fgt')

@app.get("/api")
async def autocomplete():
    print("Fastapi application")
    


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
