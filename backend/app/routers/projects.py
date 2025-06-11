from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Project
from app.schemas import ProjectCreate, ProjectOut
from app.dependencies import get_current_user
import os
import uuid

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/", response_model=ProjectOut)
def create_project(project: ProjectCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_project = Project(
        user_id=current_user.id,
        title=project.title,
        description=project.description,
        image_url=project.image_url,
        github_url=project.github_url,
        demo_url=project.demo_url,
        technologies=project.technologies
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.get("/user", response_model=list[ProjectOut])
def get_user_projects(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    projects = db.query(Project).filter(Project.user_id == current_user.id).all()
    return projects