from pydantic import BaseModel
from typing import Any, Optional

class ScriptGenerationRequest(BaseModel):
    user_stories: Any
    model_id: Optional[str] = None

class ScriptGenerationResponse(BaseModel):
    message: str
    scripts: Any 