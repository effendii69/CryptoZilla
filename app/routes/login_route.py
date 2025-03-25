from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.models.user_model import User
from app.db import users_collection
from bson import ObjectId
from typing import List

login_router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@login_router.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@login_router.post("/")
async def login(request: Request, wallet_id: str = Form(...), password: str = Form(...)):
    user = await users_collection.find_one({"wallet_id": wallet_id, "password": password})
    if user:
        response = RedirectResponse("/", status_code=303)
        response.set_cookie(key="user", value=wallet_id)
        return response
    raise HTTPException(status_code=403, detail="Invalid username or password")