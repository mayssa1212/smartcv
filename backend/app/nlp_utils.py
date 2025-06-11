import re
import random
from typing import List, Dict, Any, Optional
import spacy
from collections import Counter
import json
import os
from io import BytesIO
import docx
import pdfplumber
from fastapi import UploadFile
from huggingface_hub import InferenceClient
from app.config import Settings

# Import des modèles de base de données
from app import models

# Charger le modèle SpaCy
try:
    nlp = spacy.load("fr_core_news_md")
except OSError:
    # Fallback au modèle plus petit si le grand n'est pas disponible
    nlp = spacy.load("fr_core_news_sm")

settings = Settings()

def get_hf_client():
    """Retourne un client Hugging Face configuré avec le token d'API"""
    return InferenceClient(token=settings.HUGGINGFACE_API_KEY)

def extract_skills(text: str) -> List[str]:
    """
    Extrait les compétences d'un texte en utilisant une liste prédéfinie et NER.
    """
    # Liste de compétences courantes (à enrichir)
    common_skills = [
        "python", "java", "javascript", "html", "css", "react", "angular", "vue", 
        "node.js", "express", "django", "flask", "fastapi", "sql", "nosql", "mongodb",
        "postgresql", "mysql", "docker", "kubernetes", "aws", "azure", "gcp", "git",
        "agile", "scrum", "kanban", "jira", "confluence", "excel", "word", "powerpoint",
        "photoshop", "illustrator", "indesign", "figma", "sketch", "adobe xd",
        "marketing", "seo", "sem", "google analytics", "social media", "content writing",
        "copywriting", "project management", "team management", "leadership", "communication"
    ]
    
    # Convertir en minuscules pour la comparaison
    text_lower = text.lower()
    
    # Rechercher les compétences dans le texte
    found_skills = [skill for skill in common_skills if re.search(r'\b' + re.escape(skill) + r'\b', text_lower)]
    
    # Utiliser SpaCy pour extraire des entités supplémentaires
    doc = nlp(text)
    entities = [ent.text.lower() for ent in doc.ents if ent.label_ in ["PRODUCT", "ORG", "LANGUAGE"]]
    
    # Combiner et dédupliquer
    all_skills = list(set(found_skills + entities))
    
    return all_skills

def summarize_text(text: str) -> str:
    """
    Crée un résumé du texte en extrayant les phrases les plus importantes.
    """
    doc = nlp(text)
    
    # Calculer la fréquence des mots (sauf stopwords)
    word_freq = Counter([token.text.lower() for token in doc if not token.is_stop and not token.is_punct])
    
    # Calculer le score de chaque phrase basé sur la fréquence des mots
    sentence_scores = {}
    for sent in doc.sents:
        for word in sent:
            if word.text.lower() in word_freq:
                if sent in sentence_scores:
                    sentence_scores[sent] += word_freq[word.text.lower()]
                else:
                    sentence_scores[sent] = word_freq[word.text.lower()]
    
    # Sélectionner les 3 phrases avec les scores les plus élevés
    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:3]
    
    # Trier les phrases selon leur ordre d'apparition dans le texte
    summary = " ".join([sent.text for sent in summary_sentences])
    
    return summary

def evaluate_cv(text: str) -> Dict[str, float]:
    """
    Donne un score fictif basé sur le nombre de compétences trouvées.
    """
    score = 0.5 + 0.05 * len(extract_skills(text))
    return {"score": min(score, 1.0)}

def detect_language(text: str) -> str:
    """
    Détecte la langue de base (français, anglais, autre) de façon simplifiée.
    """
    if re.search(r"\b(le|la|et|est|vous|nous|je|de)\b", text.lower()):
        return "fr"
    elif re.search(r"\b(the|and|is|you|we|i|of)\b", text.lower()):
        return "en"
    else:
        return "unknown"

def extract_experiences(text: str) -> List[str]:
    """
    Extrait les expériences professionnelles (ligne contenant 'experience' ou 'worked at').
    """
    return [line for line in text.split("\n") if "experience" in line.lower() or "worked at" in line.lower()]

def extract_degrees(text: str) -> List[str]:
    """
    Extrait les diplômes du texte.
    """
    degrees = ["master", "licence", "bachelor", "doctorat", "phd", "bac", "bts", "dut", "ingénieur"]
    return [line for line in text.split("\n") if any(degree in line.lower() for degree in degrees)]

def suggest_skills_for_job(job_title: str) -> List[str]:
    """
    Suggère des compétences pertinentes pour un poste donné en utilisant l'IA
    """
    if not job_title:
        return ["Python", "JavaScript", "Communication", "Travail d'équipe", "Résolution de problèmes"]
    
    client = get_hf_client()
    prompt = f"""
    Suggère 5 compétences professionnelles pertinentes pour un poste de {job_title}.
    Réponds uniquement avec une liste de compétences, sans phrases d'introduction.
    """
    
    try:
        response = client.text_generation(
            prompt,
            model="mistralai/Mistral-7B-Instruct-v0.2",
            max_new_tokens=150,
            temperature=0.3,
            return_full_text=False
        )
        
        # Nettoyer et extraire les compétences
        skills_text = response.strip()
        # Diviser par lignes ou par virgules selon le format de réponse
        if "\n" in skills_text:
            skills = [s.strip().strip('- ') for s in skills_text.split("\n") if s.strip()]
        else:
            skills = [s.strip() for s in skills_text.split(",") if s.strip()]
        
        # Limiter à 5 compétences
        return skills[:5]
    except Exception as e:
        print(f"Erreur lors de la suggestion de compétences: {str(e)}")
        # Fallback à des compétences génériques
        return ["Python", "JavaScript", "Communication", "Travail d'équipe", "Résolution de problèmes"]

def compare_with_job_offers(skills: List[str], job_title: str) -> Dict[str, any]:
    """
    Compare les compétences extraites avec celles demandées dans les offres d'emploi.
    """
    # Compétences couramment demandées pour différents postes (simulation)
    job_market_skills = {
        "développeur": ["Python", "JavaScript", "Git", "SQL", "Docker", "CI/CD", "Agile"],
        "développeur web": ["HTML", "CSS", "JavaScript", "React", "Node.js", "REST API", "GraphQL"],
        "data scientist": ["Python", "R", "SQL", "Machine Learning", "TensorFlow", "Pandas", "Statistiques"],
        "designer": ["Photoshop", "Illustrator", "Figma", "UI/UX", "Sketch", "InDesign", "Design Thinking"],
        "marketing": ["SEO", "Google Analytics", "Content Marketing", "Social Media", "Email Marketing", "CRM"],
    }
    
    # Trouver le poste le plus proche
    target_skills = []
    for job, market_skills in job_market_skills.items():
        if job in job_title.lower():
            target_skills = market_skills
            break
    
    # Si aucun poste correspondant, utiliser des compétences générales
    if not target_skills:
        target_skills = ["Communication", "Travail d'équipe", "Résolution de problèmes", "Adaptabilité"]
    
    # Calculer le score de correspondance
    matching_skills = [skill for skill in skills if any(market_skill.lower() == skill.lower() for market_skill in target_skills)]
    missing_skills = [skill for skill in target_skills if not any(skill.lower() == user_skill.lower() for user_skill in skills)]
    
    match_score = len(matching_skills) / len(target_skills) if target_skills else 0
    
    return {
        "match_score": match_score,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "recommended_skills": missing_skills[:3]  # Top 3 compétences à acquérir
    }

def generate_chatbot_response(user_query: str, job_title: Optional[str] = None) -> Dict[str, Any]:
    """
    Génère une réponse de chatbot pour guider l'utilisateur dans la création de son CV
    en utilisant l'API Hugging Face
    """
    # Analyser la requête avec SpaCy pour détecter l'intention
    doc = nlp(user_query.lower())
    
    # Mots-clés pour détecter l'intention
    education_keywords = ["éducation", "formation", "diplôme", "études", "école"]
    experience_keywords = ["expérience", "travail", "emploi", "job", "poste"]
    skills_keywords = ["compétence", "savoir-faire", "aptitude", "connaissance"]
    
    # Détection basique d'intention
    next_step = ""
    if any(keyword in user_query.lower() for keyword in education_keywords):
        next_step = "education"
    elif any(keyword in user_query.lower() for keyword in experience_keywords):
        next_step = "experience"
    elif any(keyword in user_query.lower() for keyword in skills_keywords):
        next_step = "skills"
    
    # Utiliser Hugging Face pour générer une réponse personnalisée
    client = get_hf_client()
    prompt = f"""
    Tu es un assistant CV qui aide les utilisateurs à créer un CV professionnel.
    
    Question de l'utilisateur: {user_query}
    
    {f"Poste visé: {job_title}" if job_title else ""}
    
    Réponds de manière concise et professionnelle avec des conseils pratiques.
    Limite ta réponse à 3-4 phrases maximum.
    """
    
    try:
        response = client.text_generation(
            prompt,
            model="mistralai/Mistral-7B-Instruct-v0.2",
            max_new_tokens=200,
            temperature=0.7,
            return_full_text=False
        )
        
        # Générer des suggestions basées sur la réponse
        suggestions_prompt = f"""
        Basé sur cette question: "{user_query}"
        
        Et cette réponse: "{response}"
        
        Génère 3 suggestions concrètes et pratiques que l'utilisateur peut suivre.
        Chaque suggestion doit être une phrase courte et actionnable.
        Réponds uniquement avec la liste des 3 suggestions, sans phrases d'introduction.
        """
        
        suggestions_response = client.text_generation(
            suggestions_prompt,
            model="mistralai/Mistral-7B-Instruct-v0.2",
            max_new_tokens=150,
            temperature=0.5,
            return_full_text=False
        )
        
        # Nettoyer et extraire les suggestions
        suggestions_text = suggestions_response.strip()
        if "\n" in suggestions_text:
            suggestions = [s.strip().strip('- ') for s in suggestions_text.split("\n") if s.strip()]
        else:
            suggestions = [s.strip() for s in suggestions_text.split(".") if s.strip()]
        
        # Limiter à 3 suggestions
        suggestions = suggestions[:3]
        
        return {
            "message": response.strip(),
            "suggestions": suggestions,
            "next_step": next_step
        }
    except Exception as e:
        print(f"Erreur lors de la génération de réponse: {str(e)}")
        # Réponse par défaut en cas d'erreur
        return {
            "message": "Je suis désolé, je n'ai pas pu traiter votre demande. Comment puis-je vous aider avec votre CV?",
            "suggestions": [
                "Essayez de poser une question plus spécifique",
                "Demandez des conseils sur une section particulière de votre CV",
                "Précisez le poste que vous visez pour des conseils plus adaptés"
            ],
            "next_step": ""
        }

def get_job_specific_skills(job_title: str) -> List[str]:
    """
    Retourne des compétences spécifiques à un métier donné
    """
    # Dictionnaire de compétences par métier (à enrichir)
    job_skills = {
        "développeur": ["JavaScript", "Python", "Git", "SQL", "Résolution de problèmes"],
        "data scientist": ["Python", "R", "Machine Learning", "SQL", "Statistiques"],
        "marketing": ["SEO", "Réseaux sociaux", "Google Analytics", "Copywriting"],
        "designer": ["Photoshop", "Illustrator", "UI/UX", "Figma", "InDesign"]
    }
    
    # Rechercher le métier dans le dictionnaire (recherche partielle)
    for job, skills in job_skills.items():
        if job in job_title.lower():
            return skills
    
    # Métier non trouvé, retourner des compétences génériques
    return ["Communication", "Organisation", "Adaptabilité", "Travail d'équipe"]

def calculate_job_relevance(cv_text: str) -> Dict[str, float]:
    """
    Calcule un score de pertinence du CV pour différents métiers
    """
    # Liste de métiers à évaluer
    jobs = ["développeur", "data scientist", "marketing", "designer", "chef de projet", "commercial"]
    
    # Extraire les compétences du CV
    cv_skills = extract_skills(cv_text)
    
    # Calculer les scores pour chaque métier
    scores = {}
    for job in jobs:
        job_skills = get_job_specific_skills(job)
        
        # Calculer le nombre de compétences correspondantes
        matching_skills = sum(1 for skill in cv_skills if any(job_skill.lower() in skill.lower() for job_skill in job_skills))
        
        # Calculer le score (0-1)
        score = min(matching_skills / max(len(job_skills), 1), 1.0)
        scores[job] = round(score, 2)
    
    # Trier les scores par ordre décroissant
    return dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))

def suggest_cv_improvements(cv_text: str) -> Dict[str, Any]:
    """
    Analyse le CV et suggère des améliorations
    """
    # Analyser le CV avec SpaCy
    doc = nlp(cv_text)
    
    # Suggestions de style
    style_suggestions = [
        "Utilisez des verbes d'action pour décrire vos expériences",
        "Évitez les phrases à la première personne (je, mon, ma)",
        "Soyez concis et précis dans vos descriptions"
    ]
    
    # Suggestions de contenu
    content_suggestions = []
    
    # Vérifier si le CV contient des dates
    if not re.search(r'\b(19|20)\d{2}\b', cv_text):
        content_suggestions.append("Ajoutez des dates précises pour vos expériences et formations")
    
    # Vérifier si le CV contient des chiffres (résultats quantifiés)
    if not re.search(r'\b\d+%|\b\d+\s*(euros|€|k€|k)\b', cv_text):
        content_suggestions.append("Quantifiez vos résultats avec des chiffres précis")
    
    # Vérifier la présence de coordonnées
    if not re.search(r'(email|e-mail|mail|courriel|tél|tel|téléphone|telephone|portable|contact)', cv_text.lower()):
        content_suggestions.append("Ajoutez vos coordonnées complètes (email, téléphone)")
    
    # Problèmes grammaticaux (simplifiés)
    grammar_issues = []
    for sent in doc.sents:
        # Détecter les phrases très longues
        if len(sent) > 30:
            grammar_issues.append(f"Phrase trop longue: '{sent.text[:50]}...'")
    
    # Sections améliorées (exemples)
    improved_sections = {
        "expérience": "Développeur Web chez XYZ (2019-2021)\n- Développement de 3 applications web générant 25% de revenus supplémentaires\n- Optimisation des performances, réduisant les temps de chargement de 40%\n- Collaboration avec une équipe de 5 développeurs sur des projets agiles",
        "compétences": "Compétences techniques: JavaScript (React, Node.js), Python, SQL, Git\nCompétences personnelles: Communication, Résolution de problèmes, Travail d'équipe"
    }
    
    return {
        "style": style_suggestions,
        "content": content_suggestions,
        "grammar": grammar_issues,
        "improved_sections": improved_sections
    }

async def extract_text_from_pdf(file: UploadFile) -> str:
    """
    Extrait le texte d'un fichier PDF
    """
    content = await file.read()
    pdf_file = BytesIO(content)
    
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    
    return text

async def extract_text_from_docx(file: UploadFile) -> str:
    """
    Extrait le texte d'un fichier DOCX
    """
    content = await file.read()
    docx_file = BytesIO(content)
    
    doc = docx.Document(docx_file)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    
    return text

def generate_cover_letter(cv_text: str, job_title: str, company_name: str, tone: str = "professional") -> str:
    """
    Génère une lettre de motivation adaptée au poste visé
    """
    # Extraire les compétences et expériences du CV
    skills = extract_skills(cv_text)
    experiences = extract_experiences(cv_text)
    
    # Sélectionner les compétences les plus pertinentes pour le poste
    job_skills = get_job_specific_skills(job_title)
    relevant_skills = [skill for skill in skills if any(job_skill.lower() in skill.lower() for job_skill in job_skills)]
    
    # Générer l'introduction selon le ton demandé
    intros = {
        "professional": f"Madame, Monsieur,\n\nJe vous soumets ma candidature pour le poste de {job_title} au sein de {company_name}.",
        "friendly": f"Bonjour,\n\nC'est avec enthousiasme que je postule pour le poste de {job_title} chez {company_name}.",
        "enthusiastic": f"Madame, Monsieur,\n\nPassionné(e) par le domaine de {job_title.split()[0]}, je suis très enthousiaste à l'idée de rejoindre {company_name}."
    }
    
    # Générer le corps de la lettre
    body = f"Fort de mon expérience en tant que {experiences[0] if experiences else job_title}, j'ai développé des compétences en {', '.join(relevant_skills[:3] if relevant_skills else ['communication', 'organisation'])}. "
    body += f"Ces compétences, associées à mon parcours professionnel, me permettraient d'apporter une contribution significative à votre entreprise.\n\n"
    body += f"Particulièrement intéressé(e) par {company_name} pour sa réputation dans le domaine, je souhaite mettre à profit mes connaissances et mon expérience pour contribuer à vos projets innovants."
    
    # Générer la conclusion
    conclusion = "\n\nJe me tiens à votre disposition pour un entretien où je pourrai vous exposer plus en détail mes motivations et mes compétences.\n\nJe vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées."
    
    # Assembler la lettre complète
    letter = intros.get(tone, intros["professional"]) + "\n\n" + body + conclusion
    
    return letter

def analyze_personality_test(test_id: int, answers: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyse les réponses à un test de personnalité et génère un profil
    """
    # Simuler différents types de tests
    if test_id == 1:  # MBTI
        # Calculer les scores pour chaque dimension
        scores = {
            "E-I": 0,  # Extraversion vs Introversion
            "S-N": 0,  # Sensation vs Intuition
            "T-F": 0,  # Pensée vs Sentiment
            "J-P": 0   # Jugement vs Perception
        }
        
        # Analyser les réponses (simulation simplifiée)
        for question_id, answer in answers.items():
            q_id = int(question_id)
            if q_id <= 5:  # Questions E-I
                scores["E-I"] += 1 if answer > 3 else -1
            elif q_id <= 10:  # Questions S-N
                scores["S-N"] += 1 if answer > 3 else -1
            elif q_id <= 15:  # Questions T-F
                scores["T-F"] += 1 if answer > 3 else -1
            else:  # Questions J-P
                scores["J-P"] += 1 if answer > 3 else -1
        
        # Déterminer le type MBTI
        personality_type = ""
        personality_type += "I" if scores["E-I"] > 0 else "E"
        personality_type += "N" if scores["S-N"] > 0 else "S"
        personality_type += "F" if scores["T-F"] > 0 else "T"
        personality_type += "P" if scores["J-P"] > 0 else "J"
        
        # Descriptions des types MBTI (simplifiées)
        descriptions = {
            "INTJ": "Architecte - Stratège, indépendant et analytique",
            "INTP": "Logicien - Innovateur, curieux et logique",
            "ENTJ": "Commandant - Leader, décisif et stratégique",
            "ENTP": "Innovateur - Visionnaire, curieux et débatteur",
            # Autres types...
        }
        
        # Suggestions de carrière par type
        career_suggestions = {
            "INTJ": ["Architecte", "Ingénieur", "Scientifique", "Analyste"],
            "INTP": ["Développeur", "Chercheur", "Professeur", "Analyste de données"],
            "ENTJ": ["Directeur", "Entrepreneur", "Consultant", "Avocat"],
            "ENTP": ["Entrepreneur", "Avocat", "Consultant", "Marketing"],
            # Autres types...
        }
        
        return {
            "profile_type": personality_type,
            "description": descriptions.get(personality_type, f"Type {personality_type}"),
            "strengths": ["Analytique", "Stratégique", "Indépendant"],  # À personnaliser selon le type
            "weaknesses": ["Perfectionniste", "Critique", "Distant"],  # À personnaliser selon le type
            "career_suggestions": career_suggestions.get(personality_type, ["Consultant", "Analyste"]),
            "detailed_results": scores
        }
    
    elif test_id == 2:  # Big Five
        # Calculer les scores pour chaque trait
        traits = {
            "openness": 0,        # Ouverture à l'expérience
            "conscientiousness": 0, # Conscienciosité
            "extraversion": 0,    # Extraversion
            "agreeableness": 0,   # Agréabilité
            "neuroticism": 0      # Névrosisme
        }
        
        # Analyser les réponses (simulation simplifiée)
        for question_id, answer in answers.items():
            q_id = int(question_id)
            if q_id <= 6:
                traits["openness"] += answer
            elif q_id <= 12:
                traits["conscientiousness"] += answer
            elif q_id <= 18:
                traits["extraversion"] += answer
            elif q_id <= 24:
                traits["agreeableness"] += answer
            else:
                traits["neuroticism"] += answer
        
        # Normaliser les scores (0-100)
        for trait in traits:
            traits[trait] = min(100, max(0, (traits[trait] / 6) * 20))
        
        # Déterminer le trait dominant
        dominant_trait = max(traits.items(), key=lambda x: x[1])[0]
        
        # Descriptions des profils
        profiles = {
            "openness": "Ouvert à l'expérience - Créatif, curieux et innovant",
            "conscientiousness": "Consciencieux - Organisé, fiable et méthodique",
            "extraversion": "Extraverti - Sociable, énergique et assertif",
            "agreeableness": "Agréable - Coopératif, empathique et altruiste",
            "neuroticism": "Émotif - Sensible, anxieux et réactif"
        }
        
        # Suggestions de carrière par trait dominant
        career_by_trait = {
            "openness": ["Artiste", "Chercheur", "Entrepreneur", "Consultant"],
            "conscientiousness": ["Gestionnaire de projet", "Comptable", "Analyste", "Médecin"],
            "extraversion": ["Commercial", "Marketing", "Relations publiques", "Enseignant"],
            "agreeableness": ["Travailleur social", "Infirmier", "Psychologue", "RH"],
            "neuroticism": ["Écrivain", "Artiste", "Chercheur", "Analyste"]
        }
        
        return {
            "profile_type": dominant_trait.capitalize(),
            "description": profiles[dominant_trait],
            "strengths": ["Adaptabilité", "Créativité", "Curiosité"] if dominant_trait == "openness" else ["Organisation", "Fiabilité", "Persévérance"],
            "weaknesses": ["Distraction", "Impulsivité"] if dominant_trait == "openness" else ["Rigidité", "Perfectionnisme"],
            "career_suggestions": career_by_trait[dominant_trait],
            "detailed_results": traits
        }
    
    else:
        # Test non reconnu
        return {
            "profile_type": "Indéterminé",
            "description": "Type de test non reconnu",
            "strengths": [],
            "weaknesses": [],
            "career_suggestions": [],
            "detailed_results": {}
        }

def calculate_profile_completion(user_id: int, db) -> float:
    """
    Calcule le pourcentage de complétion du profil utilisateur
    """
    # Récupérer l'utilisateur et ses données associées
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return 0.0
    
    # Récupérer les CVs de l'utilisateur
    cvs = db.query(models.CV).filter(models.CV.user_id == user_id).all()
    
    # Récupérer les projets de l'utilisateur
    projects = db.query(models.Project).filter(models.Project.user_id == user_id).all()
    
    # Récupérer les résultats de tests de personnalité
    personality_results = db.query(models.PersonalityResult).filter(models.PersonalityResult.user_id == user_id).all()
    
    # Définir les critères de complétion et leur poids
    completion_criteria = {
        "user_info": 0.2,  # Informations de base de l'utilisateur
        "cv": 0.4,         # CV complet
        "projects": 0.2,   # Projets
        "personality": 0.2  # Tests de personnalité
    }
    
    # Calculer le score pour chaque critère
    scores = {
        "user_info": 1.0 if user.full_name and user.email else 0.5,
        "cv": min(1.0, len(cvs) * 0.5) if cvs else 0.0,
        "projects": min(1.0, len(projects) * 0.25) if projects else 0.0,
        "personality": min(1.0, len(personality_results) * 0.5) if personality_results else 0.0
    }
    
    # Calculer le score total pondéré
    total_score = sum(scores[criterion] * weight for criterion, weight in completion_criteria.items())
    
    # Convertir en pourcentage
    return total_score * 100








