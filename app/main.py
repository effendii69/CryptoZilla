from fastapi import FastAPI,Request
from app.routes.main_route import main_router
from app.routes.user_route import user_router
from app.routes.signup_route import signup_router
from app.routes.login_route import login_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes.api_route import api_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(main_router)
app.include_router(user_router, prefix="/users")
app.include_router(signup_router, prefix="/signup")
app.include_router(login_router, prefix="/login")
app.include_router(api_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def remove_admin_cookie_middleware(request: Request, call_next):
    response = await call_next(request)
    if not request.url.path.startswith("/admin"):
        response.delete_cookie("admin")
    return response


