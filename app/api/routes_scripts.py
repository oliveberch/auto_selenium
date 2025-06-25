from fastapi import APIRouter, Form, Body
from fastapi.responses import FileResponse, StreamingResponse
from app.schemas.scripts import ScriptGenerationRequest, ScriptGenerationResponse
from app.core.selenium_gen import generate_selenium_scripts
from app.utils.file_ops import zip_scripts
import json
from app.core.config import SELECTED_MODEL

router = APIRouter(prefix="/scripts", tags=["scripts"])

@router.post("/generate")
def generate_scripts_endpoint(
    request: ScriptGenerationRequest
):
    """
    Receives user stories and generates Selenium scripts.
    The generated scripts are zipped and returned directly for download.
    """
    user_stories_data = request.user_stories
    if isinstance(user_stories_data, str):
        user_stories_data = json.loads(user_stories_data)
    
    active_model_id = request.model_id or SELECTED_MODEL["id"]
    scripts = generate_selenium_scripts(user_stories_data, active_model_id)
    
    # After generating, immediately zip them for download
    zip_path = zip_scripts(scripts)
    zip_file = open(zip_path, "rb")
    return StreamingResponse(zip_file, media_type="application/zip", headers={"Content-Disposition": "attachment; filename=selenium_scripts.zip"})

@router.get("/download")
def download_scripts(zip_path: str):
    """Downloads the zipped scripts generated from a previous request."""
    return FileResponse(zip_path, filename="selenium_scripts.zip", media_type="application/zip") 