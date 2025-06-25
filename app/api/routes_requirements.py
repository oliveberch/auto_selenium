from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional
from app.schemas.requirements import RequirementsInput, RequirementsResponse
from fastapi.responses import JSONResponse
from app.core.config import SELECTED_MODEL

router = APIRouter(prefix="/requirements", tags=["requirements"])

@router.post("/", response_model=RequirementsResponse)
def upload_requirements(
    requirements: UploadFile = File(..., description="Requirements file (txt or md)"),
    model_id: Optional[str] = Form(None)
):
    active_model_id = model_id or SELECTED_MODEL["id"]
    content = requirements.file.read().decode("utf-8")
    # TODO: Store in session or temp storage
    return RequirementsResponse(message="Requirements received.", requirements=content, model_id=active_model_id) 