from fastapi import APIRouter, HTTPException
from app.schemas.models import (
    ModelListResponse, 
    ModelSelectionRequest, 
    ModelSelectionResponse, 
    CurrentModelResponse
)
from app.core.config import AVAILABLE_MODELS, SELECTED_MODEL

router = APIRouter(prefix="/models", tags=["models"])

@router.get("/", response_model=ModelListResponse)
def list_models():
    return ModelListResponse(models=AVAILABLE_MODELS)

@router.post("/select", response_model=ModelSelectionResponse)
def select_model(request: ModelSelectionRequest):
    """Select the model to be used for subsequent API calls."""
    if not any(model['id'] == request.model_id for model in AVAILABLE_MODELS):
        raise HTTPException(status_code=404, detail=f"Model '{request.model_id}' not found.")
    
    SELECTED_MODEL["id"] = request.model_id
    return ModelSelectionResponse(
        message=f"Model selected: {request.model_id}",
        selected_model_id=request.model_id
    )

@router.get("/current", response_model=CurrentModelResponse)
def get_current_model():
    """Get the currently selected model."""
    return CurrentModelResponse(selected_model_id=SELECTED_MODEL["id"]) 