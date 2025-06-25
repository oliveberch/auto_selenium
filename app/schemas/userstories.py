from pydantic import BaseModel
from typing import Any, List

class UserStoryRequest(BaseModel):
    requirements: str
    model_id: str
    app_url: str
    app_pages: str
    username: str
    password: str

class UserStoryResponse(BaseModel):
    message: str
    user_stories: Any

class UserStoryMatchRequest(BaseModel):
    requirements: str
    features: str
    model_id: str

class UserStoryMatchResponse(BaseModel):
    message: str
    matches: List[Any] 