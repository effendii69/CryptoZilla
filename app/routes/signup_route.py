from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.models.user_model import User
from app.db import users_collection
from bson import ObjectId
from typing import List

signup_router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@signup_router.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@signup_router.post("/")
async def create_user(wallet_id: str = Form(...), password: str = Form(...)):
    user = User(wallet_id=wallet_id, password=password)
    result = await users_collection.insert_one(user.dict(by_alias=True))
    if result.inserted_id:
        return RedirectResponse("/login", status_code=303)
    raise HTTPException(status_code=400, detail="User not created")