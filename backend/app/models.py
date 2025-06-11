from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, JSON, Float, Table, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Table d'association pour les technologies des projets
project_technologies = Table(
    "project_technologies",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id")),
    Column("technology", String)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    role = Column(String, default="user")  # "user", "admin", "recruiter"
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    cvs = relationship("CV", back_populates="user")
    projects = relationship("Project", back_populates="user")
    personality_results = relationship("PersonalityResult", back_populates="user")
    search_logs = relationship("RecruiterSearchLog", back_populates="recruiter")

class CV(Base):
    __tablename__ = "cvs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    data = Column(Text)
    skills = Column(Text, nullable=True)
    evaluation = Column(Text, nullable=True)
    file_pdf = Column(String, nullable=True)
    file_docx = Column(String, nullable=True)
    is_public = Column(Boolean, default=False)
    education_level = Column(Integer, default=0)  # 0-5 (0: aucun, 5: doctorat)
    years_experience = Column(Integer, default=0)
    location = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="cvs")
    views = relationship("CVView", back_populates="cv")
    downloads = relationship("CVDownload", back_populates="cv")

class CVView(Base):
    __tablename__ = "cv_views"

    id = Column(Integer, primary_key=True, index=True)
    cv_id = Column(Integer, ForeignKey("cvs.id"))
    viewer_ip = Column(String, nullable=True)
    viewer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    viewed_at = Column(DateTime, default=datetime.utcnow)
    
    cv = relationship("CV", back_populates="views")

class CVDownload(Base):
    __tablename__ = "cv_downloads"

    id = Column(Integer, primary_key=True, index=True)
    cv_id = Column(Integer, ForeignKey("cvs.id"))
    downloader_ip = Column(String, nullable=True)
    downloader_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    downloaded_at = Column(DateTime, default=datetime.utcnow)
    
    cv = relationship("CV", back_populates="downloads")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    description = Column(Text)
    image_url = Column(String, nullable=True)
    github_url = Column(String, nullable=True)
    demo_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="projects")
    technologies = relationship("Technology", secondary=project_technologies)

class Technology(Base):
    __tablename__ = "technologies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

class PersonalityTest(Base):
    __tablename__ = "personality_tests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    questions = Column(JSON)  # Liste de questions avec options
    
    results = relationship("PersonalityResult", back_populates="test")

class PersonalityResult(Base):
    __tablename__ = "personality_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    test_id = Column(Integer, ForeignKey("personality_tests.id"))
    results = Column(JSON)  # Résultats détaillés
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="personality_results")
    test = relationship("PersonalityTest", back_populates="results")

class RecruiterSearchLog(Base):
    __tablename__ = "recruiter_search_logs"

    id = Column(Integer, primary_key=True, index=True)
    recruiter_id = Column(Integer, ForeignKey("users.id"))
    search_params = Column(JSON)
    search_date = Column(DateTime, default=datetime.utcnow)

    recruiter = relationship("User", back_populates="search_logs")
