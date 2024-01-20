from fastapi import APIRouter, status, HTTPException, Depends, Request, UploadFile, Form
import os
from dotenv import load_dotenv
from features.bot_interface.bot import Bot
from database.supabase import supabase
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List

load_dotenv()


router = APIRouter()

bots = []

@router.post("/startUser", status_code=status.HTTP_201_CREATED)
async def start_user(username: str, phone: str, whitelist: List[str]):
    try:
        bot = Bot(phone=phone, username=username, whitelist=whitelist)
        bots.append(bot)
        asyncio.gather(bot.start())
        return { "message": "Success" }
    except Exception as e:
        print(e)

@router.post("/confirmPasscode", status_code=status.HTTP_201_CREATED)
def confirm_passcode(username: str, passcode: str):
    try:
        supabase.from_("login_passcode") \
                .insert({ "username": username, "login_passcode": passcode }) \
                .execute()
        return { "message": "Success!" }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'The following error occurred: {str(e)}'
        ) 
    
@router.post("/stopClient")
async def stop_client(username: str):
    try:
        for bot in bots:
            if bot.username == username:
                asyncio.gather(bot.stop())
                return { "messsage": "Bot successfully stopped."}
        return { "message": "Failed to stop bot."}
    except Exception as e:
        print("")
