from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional
from app.schemas.codebase import CodebaseUploadResponse, CodebaseAnalysisResponse
from fastapi.responses import JSONResponse
import tempfile
import shutil
import os
from app.core.feature_extractor import extract_features_from_codebase
import zipfile
from app.core.config import SELECTED_MODEL

router = APIRouter(prefix="/codebase", tags=["codebase"])

@router.post("/upload", response_model=CodebaseUploadResponse)
def upload_codebase(
    codebase: UploadFile = File(..., description="Codebase zip file"),
    model_id: Optional[str] = Form(None)
):
    active_model_id = model_id or SELECTED_MODEL["id"]
    # Save zip to temp dir
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, codebase.filename)
        with open(zip_path, 'wb') as f:
            shutil.copyfileobj(codebase.file, f)
        # For now, just return success
        return CodebaseUploadResponse(message="Codebase uploaded.", temp_path=zip_path, model_id=active_model_id)

@router.post("/analyze", response_model=CodebaseAnalysisResponse)
def analyze_codebase(temp_path: str = Form(...), model_id: Optional[str] = Form(None)):
    active_model_id = model_id or SELECTED_MODEL["id"]
    # Unzip if needed, then analyze
    extract_dir = temp_path + "_extracted"
    if temp_path.endswith('.zip'):
        with zipfile.ZipFile(temp_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        base_path = extract_dir
    else:
        base_path = temp_path
    features = extract_features_from_codebase(base_path)
    return CodebaseAnalysisResponse(message="Codebase analyzed.", features=features) 