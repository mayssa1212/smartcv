from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import PersonalityTest, PersonalityResult
from app.schemas import TestAnswers, PersonalityProfile
from app.dependencies import get_current_user
from typing import List, Dict

router = APIRouter(prefix="/personality", tags=["personality"])

@router.get("/tests", response_model=List[Dict])
def get_available_tests(db: Session = Depends(get_db)):
    """
    Récupère la liste des tests de personnalité disponibles
    """
    tests = db.query(PersonalityTest).all()
    return [{"id": test.id, "name": test.name, "description": test.description} for test in tests]

@router.post("/submit", response_model=PersonalityProfile)
def submit_test_answers(
    answers: TestAnswers,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Soumet les réponses à un test et génère un profil de personnalité
    """
    # Analyser les réponses et générer un profil
    profile = nlp_utils.analyze_personality_test(answers.test_id, answers.answers)
    
    # Enregistrer les résultats
    result = PersonalityResult(
        user_id=current_user.id,
        test_id=answers.test_id,
        results=profile
    )
    db.add(result)
    db.commit()
    
    return profile