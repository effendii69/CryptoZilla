# from fastapi import APIRouter, HTTPException, Request, Form
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import RedirectResponse
# from app.models.user_model import User
# from app.db import users_collection
# from bson import ObjectId
# from typing import List

# user_router = APIRouter()
# templates = Jinja2Templates(directory="app/templates")

# @user_router.post("/")
# async def create_user(wallet_id: str = Form(...), password: str = Form(...)):
#     user = User(wallet_id=wallet_id, password=password)
#     result = await users_collection.insert_one(user.dict(by_alias=True))
#     if result.inserted_id:
#         return RedirectResponse("/", status_code=303)
#     raise HTTPException(status_code=400, detail="User not created")

# @user_router.get("/{user_id}")
# async def read_user(user_id: str):
#     user = await users_collection.find_one({"_id": ObjectId(user_id)})
#     user["_id"] = str(user["_id"])
#     if user:
#         return user
#     raise HTTPException(status_code=404, detail="User not found")

# @user_router.get("/{user_id}/update")
# async def read_user(request: Request, user_id: str):
#     user = await users_collection.find_one({"_id": ObjectId(user_id)})
#     return templates.TemplateResponse("update.html", {"request": request, "user": user})


# @user_router.put("/{user_id}")
# async def update_user(user_id: str, request: Request):
#     data = await request.json()
#     wallet_id = data.get("wallet_id")
#     password = data.get("password")
#     if wallet_id is None or password is None:
#         raise HTTPException(status_code=422, detail="Name and Wallet ID are required")
#     result = await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"wallet_id": wallet_id, "password": password}})
#     if result.modified_count:
#         return RedirectResponse("/", status_code=303)
#     raise HTTPException(status_code=404, detail="User not found")

# @user_router.delete("/{user_id}")
# async def delete_user(user_id: str):
#     result = await users_collection.delete_one({"_id": ObjectId(user_id)})
#     if result.deleted_count:
#         return RedirectResponse("/", status_code=303)
#     raise HTTPException(status_code=404, detail="User not found")


from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.models.user_model import User
from app.db import users_collection
from bson import ObjectId
from typing import List

user_router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@user_router.post("/")
async def create_user(wallet_id: str = Form(...), password: str = Form(...)):
    user = User(wallet_id=wallet_id, password=password)
    result = await users_collection.insert_one(user.dict(by_alias=True))
    if result.inserted_id:
        return RedirectResponse("/", status_code=303)
    raise HTTPException(status_code=400, detail="User not created")

@user_router.get("/{user_id}")
async def read_user(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    user["_id"] = str(user["_id"])
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

@user_router.get("/{user_id}/update")
async def read_user(request: Request, user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    return templates.TemplateResponse("update.html", {"request": request, "user": user})

@user_router.put("/{user_id}")
async def update_user(user_id: str, request: Request):
    data = await request.json()
    wallet_id = data.get("wallet_id")
    password = data.get("password")
    if wallet_id is None or password is None:
        raise HTTPException(status_code=422, detail="Name and Wallet ID are required")
    result = await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"wallet_id": wallet_id, "password": password}})
    if result.modified_count:
        return RedirectResponse("/", status_code=303)
    raise HTTPException(status_code=404, detail="User not found")

@user_router.delete("/{user_id}")
async def delete_user(user_id: str):
    result = await users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count:
        return RedirectResponse("/", status_code=303)
    raise HTTPException(status_code=404, detail="User not found")

