from fastapi import APIRouter, Form, HTTPException
from typing import Optional
from app.schemas.userstories import UserStoryRequest, UserStoryResponse, UserStoryMatchRequest, UserStoryMatchResponse
from app.core.user_story import generate_user_stories, match_requirements_to_features
from app.core.config import SELECTED_MODEL, APP_CONTEXT

router = APIRouter(prefix="/userstories", tags=["userstories"])

@router.post("/generate", response_model=UserStoryResponse)
def generate_user_stories_endpoint(
    requirements: str = Form(...),
    app_url: Optional[str] = Form(None),
    app_pages: Optional[str] = Form(None),
    username: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    model_id: Optional[str] = Form(None)
):
    active_model_id = model_id or SELECTED_MODEL["id"]
    
    url = app_url or APP_CONTEXT.get("url")
    pages = app_pages or APP_CONTEXT.get("pages")
    user = username or APP_CONTEXT.get("username")
    pwd = password or APP_CONTEXT.get("password")

    if not url:
        raise HTTPException(
            status_code=400, 
            detail="Application URL must be provided either in the request or by setting the app context via POST /app-context."
        )

    user_stories = generate_user_stories(requirements, active_model_id, url, pages, user, pwd)
    return UserStoryResponse(message="User stories generated.", user_stories=user_stories)

@router.post("/match", response_model=UserStoryMatchResponse)
def match_userstories_endpoint(
    requirements: str = Form(...),
    features: str = Form(...),
    model_id: Optional[str] = Form(None)
):
    active_model_id = model_id or SELECTED_MODEL["id"]
    matches = match_requirements_to_features(requirements, features, active_model_id)
    return UserStoryMatchResponse(message="Matching complete.", matches=matches) 