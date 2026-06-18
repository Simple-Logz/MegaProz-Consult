from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(254), unique=True, nullable=False, index=True)
    full_name = Column(String(200))
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SAEnum, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class SurveyStatus(str, enum.Enum):
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class FormationType(str, enum.Enum):
    SEDIMENTARY = "sedimentary"
    IGNEOUS = "igneous"
    METAMORPHIC = "metamorphic"

class GeologicalSurvey(Base):
    __tablename__ = "geological_surveys"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    location_lat = Column(Float, nullable=False)
    location_lng = Column(Float, nullable=False)
    location_name = Column(String(200))
    status = Column(SAEnum(SurveyStatus), default=SurveyStatus.PLANNED)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    lead_geologist = Column(String(100))
    notes = Column(Text)
    metadata_json = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    drill_sites = relationship("DrillSite", back_populates="survey", cascade="all, delete-orphan")
    formations = relationship("Formation", back_populates="survey")

class Formation(Base):
    __tablename__ = "formations"
    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("geological_surveys.id"), nullable=False)
    name = Column(String(200), nullable=False)
    formation_type = Column(SAEnum(FormationType))
    depth_top_m = Column(Float)
    depth_bottom_m = Column(Float)
    age_ma = Column(Float, comment="Age in million years")
    lithology = Column(String(200))
    porosity_pct = Column(Float)
    permeability_md = Column(Float, comment="Millidarcies")
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    survey = relationship("GeologicalSurvey", back_populates="formations")
    soil_samples = relationship("SoilSample", back_populates="formation")

class DrillSite(Base):
    __tablename__ = "drill_sites"
    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("geological_surveys.id"), nullable=False)
    site_code = Column(String(50), unique=True, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    elevation_m = Column(Float)
    total_depth_m = Column(Float)
    drill_diameter_mm = Column(Float)
    drilling_method = Column(String(100))
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    survey = relationship("GeologicalSurvey", back_populates="drill_sites")
    seismic_readings = relationship("SeismicReading", back_populates="drill_site")

class SoilSample(Base):
    __tablename__ = "soil_samples"
    id = Column(Integer, primary_key=True, index=True)
    formation_id = Column(Integer, ForeignKey("formations.id"), nullable=False)
    sample_code = Column(String(50), unique=True, nullable=False)
    depth_m = Column(Float, nullable=False)
    collected_at = Column(DateTime(timezone=True))
    collected_by = Column(String(100))
    ph_level = Column(Float)
    moisture_pct = Column(Float)
    organic_matter_pct = Column(Float)
    mineral_composition = Column(JSON, default={})
    lab_results = Column(JSON, default={})
    formation = relationship("Formation", back_populates="soil_samples")

class SeismicReading(Base):
    __tablename__ = "seismic_readings"
    id = Column(Integer, primary_key=True, index=True)
    drill_site_id = Column(Integer, ForeignKey("drill_sites.id"), nullable=False)
    recorded_at = Column(DateTime(timezone=True), nullable=False)
    magnitude = Column(Float)
    depth_km = Column(Float)
    p_wave_velocity = Column(Float, comment="m/s")
    s_wave_velocity = Column(Float, comment="m/s")
    reflectivity = Column(Float)
    raw_data = Column(JSON, default={})
    drill_site = relationship("DrillSite", back_populates="seismic_readings")