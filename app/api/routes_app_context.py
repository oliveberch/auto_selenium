from fastapi import APIRouter
from app.schemas.app_context import AppContext, AppContextResponse
from app.core.config import APP_CONTEXT

router = APIRouter(prefix="/app-context", tags=["Application Context"])

@router.post("/", response_model=AppContextResponse)
def set_app_context(context: AppContext):
    """Set the application context (URL, pages, credentials) for subsequent calls."""
    APP_CONTEXT["url"] = str(context.url)
    APP_CONTEXT["pages"] = context.pages
    APP_CONTEXT["username"] = context.username
    APP_CONTEXT["password"] = context.password
    return AppContextResponse(
        message="Application context updated successfully.",
        app_context=context
    )

@router.get("/", response_model=AppContext)
def get_app_context():
    """Get the currently configured application context."""
    return AppContext(**APP_CONTEXT) 