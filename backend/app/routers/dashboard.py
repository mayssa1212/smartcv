from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import CV, CVView, CVDownload
from app.schemas import DashboardStats
from app.dependencies import get_current_user
from sqlalchemy.sql import func
from datetime import datetime, timedelta

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Récupère les statistiques pour le tableau de bord personnel
    """
    # Nombre total de CVs
    total_cvs = db.query(CV).filter(CV.user_id == current_user.id).count()
    
    # Nombre de vues des CVs (30 derniers jours)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    views = db.query(func.count(CVView.id)).filter(
        CVView.cv_id.in_(db.query(CV.id).filter(CV.user_id == current_user.id)),
        CVView.viewed_at >= thirty_days_ago
    ).scalar()
    
    # Nombre de téléchargements
    downloads = db.query(func.count(CVDownload.id)).filter(
        CVDownload.cv_id.in_(db.query(CV.id).filter(CV.user_id == current_user.id)),
        CVDownload.downloaded_at >= thirty_days_ago
    ).scalar()
    
    # Taux de complétion du profil
    profile_completion = calculate_profile_completion(db, current_user.id)
    
    return {
        "total_cvs": total_cvs,
        "views_last_30_days": views,
        "downloads_last_30_days": downloads,
        "profile_completion": profile_completion,
        "last_login": current_user.last_login
    }