from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List
from pydantic import BaseModel

from app.database import get_db
from app.auth import get_current_user
from app import models, nlp_utils

router = APIRouter(
    prefix="/assistant",
    tags=["assistant"]
)

class AssistantRequest(BaseModel):
    text: str
    job_title: str = ""
    step: str = ""

class AssistantResponse(BaseModel):
    suggestions: List[str]
    next_step: str = ""
    message: str = ""

@router.post("/guide", response_model=AssistantResponse)
def get_cv_guidance(request: AssistantRequest, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    Guide interactif pour aider à remplir le CV étape par étape
    """
    # Logique pour déterminer l'étape actuelle et les suggestions
    if request.step == "personal_info":
        return {
            "suggestions": [
                "Ajoutez votre nom complet",
                "Incluez un email professionnel",
                "Ajoutez votre numéro de téléphone"
            ],
            "next_step": "education",
            "message": "Commençons par vos informations personnelles"
        }
    elif request.step == "education":
        return {
            "suggestions": [
                "Mentionnez vos diplômes les plus récents en premier",
                "Incluez le nom de l'établissement et l'année d'obtention",
                "Ajoutez votre spécialisation"
            ],
            "next_step": "experience",
            "message": "Maintenant, parlons de votre formation"
        }
    elif request.step == "experience":
        return {
            "suggestions": [
                "Décrivez vos responsabilités avec des verbes d'action",
                "Quantifiez vos réalisations quand c'est possible",
                "Mentionnez les technologies/outils utilisés"
            ],
            "next_step": "skills",
            "message": "Passons à vos expériences professionnelles"
        }
    elif request.step == "skills":
        # Utiliser le job_title pour suggérer des compétences pertinentes
        job_skills = nlp_utils.suggest_skills_for_job(request.job_title)
        return {
            "suggestions": job_skills,
            "next_step": "summary",
            "message": f"Voici des compétences pertinentes pour un poste de {request.job_title}"
        }
    else:
        return {
            "suggestions": [
                "Commencez par vos informations personnelles",
                "Ajoutez ensuite votre formation",
                "Puis vos expériences professionnelles"
            ],
            "next_step": "personal_info",
            "message": "Bienvenue dans l'assistant CV! Suivez ces étapes pour créer un CV efficace."
        }

@router.post("/chatbot", response_model=AssistantResponse)
def cv_chatbot(request: AssistantRequest, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    Chatbot IA pour guider l'utilisateur dans la création de son CV
    """
    # Utiliser SpaCy ou Transformers pour analyser la question et générer une réponse
    user_query = request.text
    response = nlp_utils.generate_chatbot_response(user_query, request.job_title)
    
    return {
        "suggestions": response["suggestions"],
        "next_step": response["next_step"],
        "message": response["message"]
    }
