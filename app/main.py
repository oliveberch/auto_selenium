from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import (
    routes_models, routes_requirements, 
    routes_codebase, routes_userstories, 
    routes_scripts, routes_app_context,
    routes_test_plan
)


def create_app() -> FastAPI:
    app = FastAPI(title="AI-Powered Selenium Test Generator", version="2.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(routes_models.router)
    app.include_router(routes_app_context.router)
    app.include_router(routes_test_plan.router)
    app.include_router(routes_requirements.router)
    app.include_router(routes_codebase.router)
    app.include_router(routes_userstories.router)
    app.include_router(routes_scripts.router)
    return app

app = create_app() 