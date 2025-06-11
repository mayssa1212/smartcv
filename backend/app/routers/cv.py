from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import CV
from app.schemas import CVCreate, CVOut
from app.auth import get_current_user
from app import nlp_utils  # Importation correcte
# Commentez ou supprimez cette ligne si vous n'utilisez pas qrcode pour l'instant
# import qrcode
from io import BytesIO
import base64

router = APIRouter(prefix="/cv", tags=["cv"])

@router.post("/", response_model=CVOut)
def create_cv(cv: CVCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_cv = CV(user_id=current_user.id, data=cv.data)
    db.add(db_cv)
    db.commit()
    db.refresh(db_cv)
    return db_cv

@router.post("/import", response_model=CVOut)
async def import_cv(
    file: UploadFile,
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    """
    Importe un CV depuis un fichier PDF ou DOCX
    """
    # Vérifier le type de fichier
    if file.filename.endswith('.pdf'):
        cv_text = await nlp_utils.extract_text_from_pdf(file)
    elif file.filename.endswith('.docx'):
        cv_text = await nlp_utils.extract_text_from_docx(file)
    else:
        raise HTTPException(status_code=400, detail="Format de fichier non supporté")
    
    # Créer un nouveau CV avec le texte extrait
    db_cv = CV(user_id=current_user.id, data=cv_text)
    db.add(db_cv)
    db.commit()
    db.refresh(db_cv)
    return db_cv


