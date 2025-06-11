"""
Router NLP pour FastAPI : expose les endpoints d'analyse NLP pour les CV.
Importe et utilise les fonctions du module app/nlp_utils.py.
"""
from fastapi import APIRouter, HTTPException
from app.schemas import NLPAnalysis
from app import nlp_utils

router = APIRouter(
    prefix="/nlp",
    tags=["nlp"]
)

@router.post("/analyze", summary="Analyse NLP complète d'un texte")
def analyze_nlp(data: NLPAnalysis):
    """
    Endpoint principal : retourne toutes les analyses NLP (langue, compétences, résumé, évaluation, expériences, diplômes)
    """
    if not data.text:
        raise HTTPException(status_code=400, detail="Text is required.")
    return {
        "language": nlp_utils.detect_language(data.text),
        "skills": nlp_utils.extract_skills(data.text),
        "summary": nlp_utils.summarize_text(data.text),
        "evaluation": nlp_utils.evaluate_cv(data.text),
        "experiences": nlp_utils.extract_experiences(data.text),
        "degrees": nlp_utils.extract_degrees(data.text),
    }

@router.post("/skills", summary="Extraire les compétences d'un texte")
def extract_skills_endpoint(data: NLPAnalysis):
    """
    Extrait uniquement les compétences d'un texte
    """
    if not data.text:
        raise HTTPException(status_code=400, detail="Text is required.")
    return {"skills": nlp_utils.extract_skills(data.text)}

@router.post("/suggest-skills", summary="Suggérer des compétences pour un poste")
def suggest_skills_endpoint(job_title: str):
    """
    Suggère des compétences pertinentes pour un poste donné
    """
    if not job_title:
        raise HTTPException(status_code=400, detail="Job title is required.")
    return {"suggested_skills": nlp_utils.suggest_skills_for_job(job_title)}

@router.post("/compare-with-market", summary="Comparer les compétences avec le marché")
def compare_with_market(skills: list[str], job_title: str):
    """
    Compare les compétences avec celles demandées sur le marché pour un poste donné
    """
    if not skills or not job_title:
        raise HTTPException(status_code=400, detail="Skills and job title are required.")
    return nlp_utils.compare_with_job_offers(skills, job_title)

@router.post("/job-relevance-score", summary="Calculer le score de pertinence pour différents métiers")
def job_relevance_score(data: NLPAnalysis):
    """
    Calcule un score de pertinence du CV pour différents métiers
    """
    if not data.text:
        raise HTTPException(status_code=400, detail="Text is required.")
    
    # Analyser le CV et calculer des scores pour différents métiers
    return {"job_scores": nlp_utils.calculate_job_relevance(data.text)}

@router.post("/improve-cv", summary="Suggestions d'améliorations pour le CV")
def improve_cv(data: NLPAnalysis):
    """
    Analyse le CV et suggère des améliorations
    """
    if not data.text:
        raise HTTPException(status_code=400, detail="Text is required.")
    
    improvements = nlp_utils.suggest_cv_improvements(data.text)
    return {
        "style_suggestions": improvements["style"],
        "content_suggestions": improvements["content"],
        "grammar_issues": improvements["grammar"],
        "improved_sections": improvements["improved_sections"]
    }
