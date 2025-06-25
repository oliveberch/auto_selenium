from pydantic import BaseModel
from typing import List, Any

class CodebaseUploadResponse(BaseModel):
    message: str
    temp_path: str
    model_id: str

class CodebaseAnalysisResponse(BaseModel):
    message: str
    features: List[Any] 