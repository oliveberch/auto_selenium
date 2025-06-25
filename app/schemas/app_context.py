from pydantic import BaseModel
from typing import Optional

class AppContext(BaseModel):
    url: str
    pages: str
    username: Optional[str] = None
    password: Optional[str] = None

class AppContextResponse(BaseModel):
    message: str
    app_context: AppContext 