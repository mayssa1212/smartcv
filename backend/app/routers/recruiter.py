from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import CV, User, RecruiterSearchLog
from app.schemas import PublicCVOut, RecruiterSearchParams
from app.dependencies import get_current_user, check_recruiter_role
from typing import List
from datetime import datetime

router = APIRouter(prefix="/recruiter", tags=["recruiter"])

def log_recruiter_search(db: Session, recruiter_id: int, params: RecruiterSearchParams):
    """
    Enregistre les recherches effectuées par les recruteurs pour les statistiques
    """
    search_log = RecruiterSearchLog(
        recruiter_id=recruiter_id,
        search_params={
            "skills": params.skills,
            "education_level": params.education_level,
            "min_experience": params.min_experience,
            "location": params.location
        },
        search_date=datetime.now()
    )
    db.add(search_log)
    db.commit()

@router.get("/search", response_model=List[PublicCVOut], dependencies=[Depends(check_recruiter_role)])
def search_public_cvs(
    params: RecruiterSearchParams = Depends(),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Recherche des CVs publics selon différents critères
    """
    query = db.query(CV).join(User).filter(CV.is_public == True)
    
    # Filtrer par compétences
    if params.skills:
        for skill in params.skills:
            query = query.filter(CV.skills.contains(skill))
    
    # Filtrer par niveau d'études
    if params.education_level:
        query = query.filter(CV.education_level >= params.education_level)
    
    # Filtrer par années d'expérience
    if params.min_experience:
        query = query.filter(CV.years_experience >= params.min_experience)
    
    # Filtrer par localisation
    if params.location:
        query = query.filter(CV.location.contains(params.location))
    
    # Pagination
    results = query.offset(params.skip).limit(params.limit).all()
    
    # Enregistrer cette recherche pour les statistiques
    log_recruiter_search(db, current_user.id, params)
    
    return results

