from fastapi import APIRouter, Form, File, UploadFile, HTTPException
from typing import Optional
import tempfile
import shutil
import zipfile
import os
from app.core.config import SELECTED_MODEL, APP_CONTEXT
from app.core.feature_extractor import extract_features_from_codebase
from app.core.user_story import create_comprehensive_test_plan

router = APIRouter(prefix="/test-plan", tags=["Test Plan Generation"])

@router.post("/generate", response_model=dict)
def generate_test_plan(
    codebase: UploadFile = File(...),
    requirements: str = Form(""),
    model_id: Optional[str] = Form(None)
):
    """
    Generates a comprehensive test plan by analyzing a codebase,
    comparing it against user requirements, and creating a unified
    set of user stories for testing.
    """
    active_model_id = model_id or SELECTED_MODEL["id"]
    
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, 'codebase.zip')
        with open(zip_path, 'wb') as f:
            shutil.copyfileobj(codebase.file, f)
        
        extract_dir = os.path.join(tmpdir, "extracted")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            
        # 1. Extract features from the codebase
        features = extract_features_from_codebase(extract_dir)
        
        # Sanitize requirements input
        if isinstance(requirements, str):
            requirements_list = [r.strip() for r in requirements.split('\n') if r.strip()]
        else:
            requirements_list = requirements
        
        # 2. Call the new orchestrator to create the test plan
        test_plan = create_comprehensive_test_plan(
            requirements=requirements_list,
            features=features,
            model_id=active_model_id,
            app_context=APP_CONTEXT
        )
        
        if not test_plan or not test_plan.get('backlog'):
            raise HTTPException(status_code=500, detail="Failed to generate a valid test plan.")
            
        return test_plan 