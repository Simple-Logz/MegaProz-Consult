from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models
from app.schemas import FormationCreate, FormationResponse
from app.auth import get_current_user

router = APIRouter(prefix="/formations", tags=["Formations"])

@router.get("/", response_model=List[FormationResponse])
def list_formations(survey_id: int = None, db: Session = Depends(get_db), _u = Depends(get_current_user)):
    q = db.query(models.Formation)
    if survey_id:
        q = q.filter_by(survey_id=survey_id)
    return q.all()

@router.post("/", response_model=FormationResponse, status_code=status.HTTP_201_CREATED)
def create_formation(payload: FormationCreate, db: Session = Depends(get_db), _u = Depends(get_current_user)):
    f = models.Formation(**payload.model_dump())
    db.add(f); db.commit(); db.refresh(f)
    return f

@router.get("/{formation_id}", response_model=FormationResponse)
def get_formation(formation_id: int, db: Session = Depends(get_db), _u = Depends(get_current_user)):
    f = db.query(models.Formation).filter_by(id=formation_id).first()
    if not f: raise HTTPException(404, "Formation not found")
    return f

@router.get("/{formation_id}/samples")
def formation_samples(formation_id: int, db: Session = Depends(get_db), _u = Depends(get_current_user)):
    f = db.query(models.Formation).filter_by(id=formation_id).first()
    if not f: raise HTTPException(404, "Formation not found")
    return {"formation_id": formation_id, "samples": [{"id": s.id, "code": s.sample_code, "depth_m": s.depth_m, "ph": s.ph_level} for s in f.soil_samples]}