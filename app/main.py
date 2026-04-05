from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database import engine, Base
import os
from contextlib import asynccontextmanager

# We will create tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    from app import models
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="BondSync", lifespan=lifespan)

# Mount static files
import pathlib
static_path = pathlib.Path(__file__).parent.parent / "static"
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

templates_path = pathlib.Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_path))

# Include Routers
from app.routes import auth_routes, data_routes, analysis_routes
app.include_router(auth_routes.router)
app.include_router(data_routes.router)
app.include_router(analysis_routes.router)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.get("/signup")
async def signup_page(request: Request):
    return templates.TemplateResponse(request=request, name="signup.html")

@app.get("/dashboard")
async def dashboard_page(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html")
