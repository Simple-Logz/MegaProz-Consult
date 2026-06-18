from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import models
from app.schemas import SurveyCreate, SurveyUpdate, SurveyResponse
from app.auth import get_current_user

router = APIRouter(prefix="/surveys", tags=["Geological Surveys"])

@router.get("/", response_model=List[SurveyResponse])
def list_surveys(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    _user = Depends(get_current_user)
):
    """List all geological surveys with optional status filter."""
    q = db.query(models.GeologicalSurvey)
    if status:
        q = q.filter(models.GeologicalSurvey.status == status)
    return q.offset(skip).limit(limit).all()

@router.post("/", response_model=SurveyResponse, status_code=status.HTTP_201_CREATED)
def create_survey(payload: SurveyCreate, db: Session = Depends(get_db), _user = Depends(get_current_user)):
    """Create a new geological survey."""
    survey = models.GeologicalSurvey(**payload.model_dump())
    db.add(survey); db.commit(); db.refresh(survey)
    return survey

@router.get("/{survey_id}", response_model=SurveyResponse)
def get_survey(survey_id: int, db: Session = Depends(get_db), _user = Depends(get_current_user)):
    survey = db.query(models.GeologicalSurvey).filter_by(id=survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail=f"Survey {survey_id} not found")
    return survey

@router.patch("/{survey_id}", response_model=SurveyResponse)
def update_survey(survey_id: int, payload: SurveyUpdate, db: Session = Depends(get_db), _user = Depends(get_current_user)):
    survey = db.query(models.GeologicalSurvey).filter_by(id=survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(survey, k, v)
    db.commit(); db.refresh(survey)
    return survey

@router.delete("/{survey_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_survey(survey_id: int, db: Session = Depends(get_db), _user = Depends(get_current_user)):
    survey = db.query(models.GeologicalSurvey).filter_by(id=survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    db.delete(survey); db.commit()

@router.get("/{survey_id}/summary")
def survey_summary(survey_id: int, db: Session = Depends(get_db), _user = Depends(get_current_user)):
    """Aggregate summary: drill sites, formations, sample count."""
    survey = db.query(models.GeologicalSurvey).filter_by(id=survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    return {
        "survey_id": survey_id,
        "name": survey.name,
        "status": survey.status,
        "drill_sites_count": len(survey.drill_sites),
        "formations_count": len(survey.formations),
        "total_samples": sum(len(f.soil_samples) for f in survey.formations),
    }