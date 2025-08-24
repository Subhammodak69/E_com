import importlib
import pkgutil
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ['http://localhost:8000']

app.add_middleware(CORSMiddleware, allow_origins=origins)


# Dynamically import all router objects from controllers package
import controllers

for _, module_name, _ in pkgutil.iter_modules(controllers.__path__):
    module = importlib.import_module(f"controllers.{module_name}")
    if hasattr(module, "router"):
        app.include_router(module.router)
