import importlib
import pkgutil
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
import secrets

secret_key = secrets.token_urlsafe(32)




import pkgutil
import importlib
import controllers

def include_subpackage_routers(package):
    for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
        full_module_name = f"{package.__name__}.{module_name}"
        module = importlib.import_module(full_module_name)
        if hasattr(module, "router"):
            app.include_router(module.router)
        if is_pkg:
            # Recursively include routers in subpackages
            include_subpackage_routers(module)

# Call the function
include_subpackage_routers(controllers)
