from features.bot_interface.bot import Bot
import os
from features.bot_interface.bot_utils import get_phone_passcode
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from features.user.user_router import router as user_router

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router, prefix="/user", tags=["User"])

if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application using uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)