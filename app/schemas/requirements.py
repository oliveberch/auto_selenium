from pydantic import BaseModel

class RequirementsInput(BaseModel):
    requirements: str
    model_id: str

class RequirementsResponse(BaseModel):
    message: str
    requirements: str
    model_id: str 