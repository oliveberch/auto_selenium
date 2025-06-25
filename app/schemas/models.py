from pydantic import BaseModel
from typing import List

class ModelInfo(BaseModel):
    name: str
    id: str

class ModelListResponse(BaseModel):
    models: List[ModelInfo]

class ModelSelectionRequest(BaseModel):
    model_id: str

class ModelSelectionResponse(BaseModel):
    message: str
    selected_model_id: str
    
class CurrentModelResponse(BaseModel):
    selected_model_id: str 