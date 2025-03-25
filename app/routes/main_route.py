# from fastapi import APIRouter, HTTPException, Request, Form, Response
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import RedirectResponse
# from fastapi.middleware.cors import CORSMiddleware
# from app.models.user_model import User
# from app.db import collection
# from bson import ObjectId
# from typing import List

# main_router = APIRouter()
# templates = Jinja2Templates(directory="app/templates")

# @main_router.get("/")
# def read_root(request: Request):
#     user = request.cookies.get('user')
#     return templates.TemplateResponse("index.html", {"request": request, "user": user})

# @main_router.get("/admin-login")
# def admin_login(request: Request):
#     return templates.TemplateResponse("admin-login.html", {"request": request})

# @main_router.post("/admin-login")
# def admin_login_post(request: Request, admin_id: str = Form(...), password: str = Form(...)):
#     if admin_id == "admin" and password == "admin":
#         response = RedirectResponse("/admin", status_code=303)
#         response.set_cookie("admin", "true")
#         return response
#     else:
#         return templates.TemplateResponse("admin-login.html", {"request": request, "error": "Invalid credentials"})

# @main_router.get("/admin")
# async def read_root(request: Request):
#     admin = request.cookies.get('admin')
#     if not admin:
#         return RedirectResponse("/admin-login", status_code=303)
#     users = await collection.find().to_list(100)
#     return templates.TemplateResponse("user-crud.html", {"request": request, "users": users})

# @main_router.get("/dashboard")
# def get_dashboard(request: Request):
#     user = request.cookies.get('user')
#     if not user:
#         return RedirectResponse("/login", status_code=303)
#     return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})

# @main_router.post("/select-account")
# def select_account(request: Request, account_type: str = Form(...), account_size: str = Form(...)):
#     user = request.cookies.get('user')
#     if not user:
#         return RedirectResponse("/login", status_code=303)
    
#     response = RedirectResponse("/select-instruments", status_code=303)
#     response.set_cookie("account_type", account_type)
#     response.set_cookie("account_size", account_size)
#     return response

# @main_router.get("/select-instruments")
# def get_select_instruments(request: Request):
#     user = request.cookies.get('user')
#     if not user:
#         return RedirectResponse("/login", status_code=303)
#     account_type = request.cookies.get('account_type')
#     account_size = request.cookies.get('account_size')
#     return templates.TemplateResponse("instrument.html", {"request": request, "user": user, "account_type": account_type, "account_size": account_size})

# @main_router.post("/calculate-profit-loss")
# async def calculate_profit_loss(request: Request, instrument: str = Form(...), amount: float = Form(...), buying_price: float = Form(...), current_price: float = Form(...)):
#     user = request.cookies.get('user')
#     profit_loss = (current_price - buying_price) * amount
#     status = "Profit" if profit_loss > 0 else "Loss"
#     return templates.TemplateResponse("result.html", {"request": request, "user": user, "instrument": instrument, "amount": amount, "buying_price": buying_price, "current_price": current_price, "profit_loss": profit_loss, "status": status})

# @main_router.get("/logout")
# def logout(request: Request):
#     response = RedirectResponse("/", status_code=303)
#     response.delete_cookie("user")
#     response.delete_cookie("account_type")
#     response.delete_cookie("account_size")
#     response.delete_cookie("admin")
#     return response

# @main_router.get("/aboutdeveloper")
# def about_developers(request: Request):
#     return templates.TemplateResponse("aboutdeveloper.html", {"request": request})

# @main_router.get("/back-to-home")
# def back_to_home(request: Request):
#     response = RedirectResponse("/", status_code=303)
#     response.delete_cookie("admin")
#     return response
    
# # adding yahn se hogi
# @main_router.get("/add-instrument")
# def add_instrument(request: Request):
#     user = request.cookies.get('user')
#     if not user:
#         return RedirectResponse("/login", status_code=303)
#     return RedirectResponse("/select-instrument", status_code=303)

from fastapi import APIRouter, HTTPException, Request, Form, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.db import users_collection, instruments_collection
from bson import ObjectId
from typing import List
from starlette.status import HTTP_302_FOUND
# from itsdangerous import URLSafeTimedSerializer, BadSignature

# SECRET_KEY = "azam121"
# serializer = URLSafeTimedSerializer(SECRET_KEY)

# -----
main_router = APIRouter()
templates = Jinja2Templates(directory="app/templates")





@main_router.get("/")
def read_root(request: Request):
    user = request.cookies.get('user')
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

@main_router.get("/admin-login")
def admin_login(request: Request):
    return templates.TemplateResponse("admin-login.html", {"request": request})

@main_router.post("/admin-login")
def admin_login_post(request: Request, admin_id: str = Form(...), password: str = Form(...)):
    if admin_id == "admin" and password == "admin":
        response = RedirectResponse("/admin", status_code=303)
        response.set_cookie("admin", "true")
        return response
    else:
        return templates.TemplateResponse("admin-login.html", {"request": request, "error": "Invalid credentials"})

@main_router.get("/admin")
async def read_admin(request: Request):
    admin = request.cookies.get('admin')
    if not admin:
        return RedirectResponse("/admin-login", status_code=303)
    users = await users_collection.find().to_list(100)
    return templates.TemplateResponse("user-crud.html", {"request": request, "users": users})

@main_router.get("/dashboard")
async def get_dashboard(request: Request):
    user = request.cookies.get('user')
    if not user:
        return RedirectResponse("/login", status_code=303)
    instruments = await instruments_collection.find({"user": user}).to_list(100)
    total_pnl = sum(inst['profit_loss'] for inst in instruments)
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user, "instruments": instruments, "total_pnl": total_pnl})

@main_router.post("/select-account")
def select_account(request: Request, account_type: str = Form(...), account_size: str = Form(...)):
    user = request.cookies.get('user')
    if not user:
        return RedirectResponse("/login", status_code=303)
    
    response = RedirectResponse("/select-instruments", status_code=303)
    response.set_cookie("account_type", account_type)
    response.set_cookie("account_size", account_size)
    return response

@main_router.get("/select-instruments")
def get_select_instruments(request: Request):
    user = request.cookies.get('user')
    if not user:
        return RedirectResponse("/login", status_code=303)
    account_type = request.cookies.get('account_type')
    account_size = request.cookies.get('account_size')
    return templates.TemplateResponse("instrument.html", {"request": request, "user": user, "account_type": account_type, "account_size": account_size})

@main_router.post("/calculate-profit-loss")
async def calculate_profit_loss(request: Request, instrument: str = Form(...), amount: float = Form(...), buying_price: float = Form(...), current_price: float = Form(...)):
    user = request.cookies.get('user')
    profit_loss = (current_price - buying_price) * amount
    status = "Profit" if profit_loss > 0 else "Loss"

    new_instrument = {
        "instrument": instrument,
        "amount": amount,
        "buying_price": buying_price,
        "current_price": current_price,
        "profit_loss": profit_loss,
        "user": user
    }
    await instruments_collection.insert_one(new_instrument)

    instruments = await instruments_collection.find({"user": user}).to_list(100)
    total_pnl = sum(inst['profit_loss'] for inst in instruments)
    
    return templates.TemplateResponse("result.html", {
        "request": request, "user": user, "instruments": instruments, "total_pnl": total_pnl, "profit_loss": profit_loss
    })

@main_router.get("/calculate-profit-loss")
async def get_wallet_result(request: Request):
    user = request.cookies.get('user')
    if not user:
        return RedirectResponse("/login", status_code=303)

    # Fetch the instruments for the user
    instruments = await instruments_collection.find({"user": user}).to_list(100)
    
    # Convert ObjectId to string
    for inst in instruments:
        inst['_id'] = str(inst['_id'])

    # Calculate the total holdings and profit/loss for each instrument
    total_holdings = sum(inst['current_price'] * inst['amount'] for inst in instruments if inst['current_price'] and inst['amount'])
    total_pnl = sum(inst['profit_loss'] for inst in instruments if inst['profit_loss'])

    return templates.TemplateResponse("result.html", {
        "request": request,
        "user": user,
        "instruments": instruments,
        "total_holdings": total_holdings,
        "total_pnl": total_pnl
    })




@main_router.post("/delete-instrument/{instrument_id}")
async def delete_instrument(request: Request, instrument_id: str):
    result = await instruments_collection.delete_one({"_id": ObjectId(instrument_id)})
    if result.deleted_count:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Instrument not found")


@main_router.get("/update-instrument/{instrument_id}")
async def get_update_instrument(request: Request, instrument_id: str):
    instrument = await instruments_collection.find_one({"_id": ObjectId(instrument_id)})
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")
    return templates.TemplateResponse("update_instrument.html", {"request": request, "instrument": instrument})

@main_router.post("/update-instrument/{instrument_id}")
async def update_instrument(request: Request, instrument_id: str, amount: float = Form(...), buying_price: float = Form(...), current_price: float = Form(...)):
    profit_loss = (current_price - buying_price) * amount
    result = await instruments_collection.update_one(
        {"_id": ObjectId(instrument_id)},
        {"$set": {"amount": amount, "buying_price": buying_price, "current_price": current_price, "profit_loss": profit_loss}}
    )
    if result.modified_count:
        return RedirectResponse("/dashboard", status_code=303)
    raise HTTPException(status_code=404, detail="Instrument not found")

@main_router.get("/logout")
def logout(request: Request):
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("user")
    response.delete_cookie("account_type")
    response.delete_cookie("account_size")
    response.delete_cookie("admin")
    return response

@main_router.get("/aboutdeveloper")
def about_developers(request: Request):
    return templates.TemplateResponse("aboutdeveloper.html", {"request": request})

@main_router.get("/back-to-home")
def back_to_home(request: Request):
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("admin")
    return response

@main_router.get("/add-instrument")
def add_instrument(request: Request):
    user = request.cookies.get('user')
    if not user:
        return RedirectResponse("/login", status_code=303)
    return RedirectResponse("/select-instruments", status_code=303)

@main_router.get("/analytics")
async def get_analytics(request: Request):
    user = request.cookies.get('user')
    if not user:
        return RedirectResponse("/login", status_code=303)
    
    # Fetch the instruments for the user
    instruments = await instruments_collection.find({"user": user}).to_list(100)
    
    # Calculate the total holdings
    total_holdings = sum(inst['current_price'] * inst['amount'] for inst in instruments if inst['current_price'] and inst['amount'])
    
    # Calculate the percentage holdings
    holdings_data = [
        {
            "instrument": inst['instrument'],
            "percentage": (inst['current_price'] * inst['amount'] / total_holdings) * 100
        }
        for inst in instruments if total_holdings > 0
    ]
    
    # Calculate top performers
    top_performers = sorted(instruments, key=lambda x: x['profit_loss'], reverse=True)[:5]
    
    # Convert ObjectId to string
    for performer in top_performers:
        performer['_id'] = str(performer['_id'])
    
    #  performance metrics
    total_investment = sum(inst['buying_price'] * inst['amount'] for inst in instruments if inst['buying_price'] and inst['amount'])
    total_profit_loss = sum(inst['profit_loss'] for inst in instruments if inst['profit_loss'])
    average_return = (total_profit_loss / total_investment) * 100 if total_investment else 0
    
    # Prepare data for performance over time (dummy data for illustration)
    performance_over_time = [
        {"date": "2023-01-01", "profit_loss": 1000},
        {"date": "2023-02-01", "profit_loss": 1500},
        {"date": "2023-03-01", "profit_loss": 1200},
        {"date": "2023-04-01", "profit_loss": 1800},
        {"date": "2023-05-01", "profit_loss": 2000}
    ]
    
    return templates.TemplateResponse("analytics.html", {
        "request": request,
        "user": user,
        "holdings_data": holdings_data,
        "top_performers": top_performers,
        "total_investment": total_investment,
        "total_profit_loss": total_profit_loss,
        "average_return": average_return,
        "performance_over_time": performance_over_time
    })

@main_router.get("/contact")
async def contact(request: Request):
    user = request.cookies.get('user')
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("contact.html", {"request": request, "user": user})

@main_router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@main_router.post("/login")
async def login(request: Request, wallet_id: str = Form(...), password: str = Form(...)):
    user = await users_collection.find_one({"wallet_id": wallet_id})
    if not user or user["password"] != password:
        error = "Invalid username or password"
        return templates.TemplateResponse("login.html", {"request": request, "error": error})

    response = RedirectResponse("/dashboard", status_code=HTTP_302_FOUND)
    response.set_cookie(key="user", value=str(user["_id"]))
    return response


