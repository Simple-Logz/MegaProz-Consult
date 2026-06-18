from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models
from app.schemas import SoilSampleCreate, SoilSampleResponse
from app.auth import get_current_user

router = APIRouter(prefix="/samples", tags=["Soil Samples"])

@router.post("/", response_model=SoilSampleResponse, status_code=201)
def create_sample(payload: SoilSampleCreate, db: Session = Depends(get_db), _u = Depends(get_current_user)):
    existing = db.query(models.SoilSample).filter_by(sample_code=payload.sample_code).first()
    if existing:
        raise HTTPException(409, f"Sample code '{payload.sample_code}' already exists")
    s = models.SoilSample(**payload.model_dump())
    db.add(s); db.commit(); db.refresh(s)
    return s

@router.get("/{sample_id}", response_model=SoilSampleResponse)
def get_sample(sample_id: int, db: Session = Depends(get_db), _u = Depends(get_current_user)):
    s = db.query(models.SoilSample).filter_by(id=sample_id).first()
    if not s: raise HTTPException(404, "Sample not found")
    return s

@router.patch("/{sample_id}/lab-results")
def update_lab_results(sample_id: int, results: dict, db: Session = Depends(get_db), _u = Depends(get_current_user)):
    s = db.query(models.SoilSample).filter_by(id=sample_id).first()
    if not s: raise HTTPException(404, "Sample not found")
    s.lab_results = {**(s.lab_results or {}), **results}
    db.commit(); db.refresh(s)
    return {"sample_id": sample_id, "lab_results": s.lab_results}