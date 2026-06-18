from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models import SurveyStatus, FormationType

class SurveyBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    location_lat: float = Field(..., ge=-90, le=90)
    location_lng: float = Field(..., ge=-180, le=180)
    location_name: Optional[str] = None
    status: SurveyStatus = SurveyStatus.PLANNED
    lead_geologist: Optional[str] = None
    notes: Optional[str] = None

class SurveyCreate(SurveyBase): pass
class SurveyUpdate(SurveyBase):
    name: Optional[str] = None
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None

class SurveyResponse(SurveyBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

class FormationBase(BaseModel):
    survey_id: int
    name: str = Field(..., min_length=2)
    formation_type: Optional[FormationType] = None
    depth_top_m: Optional[float] = Field(None, ge=0)
    depth_bottom_m: Optional[float] = Field(None, ge=0)
    age_ma: Optional[float] = None
    lithology: Optional[str] = None
    porosity_pct: Optional[float] = Field(None, ge=0, le=100)
    permeability_md: Optional[float] = None
    description: Optional[str] = None

class FormationCreate(FormationBase): pass
class FormationResponse(FormationBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime

class SoilSampleBase(BaseModel):
    formation_id: int
    sample_code: str
    depth_m: float = Field(..., ge=0)
    ph_level: Optional[float] = Field(None, ge=0, le=14)
    moisture_pct: Optional[float] = Field(None, ge=0, le=100)
    organic_matter_pct: Optional[float] = Field(None, ge=0, le=100)
    mineral_composition: Optional[Dict[str, Any]] = {}
    lab_results: Optional[Dict[str, Any]] = {}

class SoilSampleCreate(SoilSampleBase): pass
class SoilSampleResponse(SoilSampleBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class SeismicReadingCreate(BaseModel):
    drill_site_id: int
    recorded_at: datetime
    magnitude: Optional[float] = None
    depth_km: Optional[float] = None
    p_wave_velocity: Optional[float] = None
    s_wave_velocity: Optional[float] = None
    reflectivity: Optional[float] = None

class SeismicReadingResponse(SeismicReadingCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int