import uuid
from typing import List, Optional
from fastapi_users import schemas
from pydantic import BaseModel
from uuid import UUID


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


# Asset Hunter Schemas

class ScanRequest(BaseModel):
    target_url: str
    scan_type: str = "all"  # "github", "chrome", "all"

class Asset(BaseModel):
    id: str
    name: str
    type: str  # "github_zombie", "chrome_ghost"
    url: str
    description: str
    detected_at: str
    status: str = "active"

class ScanResult(BaseModel):
    assets: List[Asset]
    total_found: int

class AnalysisRequest(BaseModel):
    asset_id: str
    asset_data: Asset

class AnalysisResult(BaseModel):
    valuation: str
    reasoning: str
    details: str
